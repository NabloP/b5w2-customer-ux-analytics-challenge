# src/nlp/sentiment_classifier.py

"""
sentiment_classifier.py – Ensemble Sentiment Analysis Module (B5W2)
--------------------------------------------------------------------
Combines DistilBERT, VADER, and TextBlob into an equal-weight ensemble.
Applies star-rating rules and flags mismatches for quality control.

Responsibilities:
- Load DistilBERT SST-2 model (PyTorch)
- Compute scaled scores from DistilBERT, VADER, and TextBlob
- Build an equal-weight ensemble score and label
- Compute uncertainty (std. deviation) across scorers
- Apply rating-based rule labels and flag significant disagreements
- Expose run() to augment a DataFrame of reviews with sentiment fields

Author: Nabil Mohamed
"""

import os  # File checks
import numpy as np  # Numeric operations
import pandas as pd  # Data handling
import torch  # PyTorch for model inference
from transformers import AutoTokenizer, AutoModelForSequenceClassification  # DistilBERT
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer  # VADER
from textblob import TextBlob  # TextBlob polarity
from typing import Optional, Dict  # Type hints


class SentimentEnsembler:
    """
    Orchestrates ensemble sentiment analysis across multiple methods.
    """

    def __init__(self, model_path: str, device: Optional[str] = None):
        """
        Initialize the ensemble with DistilBERT, VADER, and TextBlob.

        Parameters:
        -----------
        model_path : str
            Path or HF repo_id for the SST-2 fine-tuned DistilBERT model.
        device : Optional[str]
            Torch device (e.g., 'cpu' or 'cuda'). Defaults to 'cpu'.
        """
        # Determine torch device
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        # Load DistilBERT tokenizer & model to device
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.to(self.device)
        # Initialize VADER analyzer
        self.vader = SentimentIntensityAnalyzer()

    def _bert_score(self, text: str) -> float:
        """
        Compute a signed score in [-1,+1] from DistilBERT SST-2.

        Uses softmax over logits: (P_pos - P_neg).
        """
        # Tokenize text into input IDs and attention mask
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, padding=True
        )
        # Move inputs to the correct device
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        # Perform inference without gradient tracking
        with torch.no_grad():
            logits = self.model(**inputs).logits.squeeze().cpu().numpy()
        # Convert logits to probabilities via softmax
        probs = np.exp(logits) / np.exp(logits).sum()
        # Return difference (pos minus neg) for a signed score
        return float(probs[1] - probs[0])

    def _vader_score(self, text: str) -> float:
        """
        Return VADER compound score in [-1,+1].
        """
        return float(self.vader.polarity_scores(text)["compound"])

    def _textblob_score(self, text: str) -> float:
        """
        Return TextBlob polarity in [-1,+1].
        """
        return float(TextBlob(text).sentiment.polarity)

    def compute_ensemble(self, text: str) -> Dict[str, float]:
        """
        Compute individual scores, ensemble, label, and uncertainty.

        Returns:
        --------
        Dict containing:
          - bert, vader, textblob: individual scores
          - ensemble: equal-weight average
          - label: 'positive'/'neutral'/'negative'
          - uncertainty: std. deviation of [bert, vader, textblob]
        """
        # Get each model's score
        b_score = self._bert_score(text)
        v_score = self._vader_score(text)
        t_score = self._textblob_score(text)
        # Equal-weight ensemble mean
        ensemble_score = (b_score + v_score + t_score) / 3.0
        # Compute uncertainty as standard deviation
        uncertainty = float(np.std([b_score, v_score, t_score]))
        # Determine label with thresholds
        if ensemble_score >= 0.05:
            label = "positive"
        elif ensemble_score <= -0.05:
            label = "negative"
        else:
            label = "neutral"
        # Return full sentiment record
        return {
            "bert": b_score,
            "vader": v_score,
            "textblob": t_score,
            "ensemble": ensemble_score,
            "label": label,
            "uncertainty": uncertainty,
        }

    def apply_rating_rule(self, ensemble_label: str, rating: int) -> str:
        """
        Map star rating to allowed labels, enforcing business rules.

        Returns:
        --------
        rule_label: The label derived from rating constraints.
        """
        # Define allowed labels per rating
        if rating >= 5:
            allowed = {"positive", "neutral", "negative"}
        elif rating == 4:
            allowed = {"positive", "neutral", "negative"}
        elif rating == 3:
            allowed = {"positive", "neutral", "negative"}
        elif rating == 2:
            allowed = {"neutral", "negative"}
        else:  # rating == 1
            allowed = {"negative"}
        # If ensemble label allowed, keep it; else fallback to nearest allowed
        return ensemble_label if ensemble_label in allowed else "neutral"

    def flag_disagreement(
        self, ens_label: str, rule_label: str, ens_score: float, threshold: float = 0.5
    ) -> bool:
        """
        Flag reviews where ensemble label disagrees with rating rule
        and ensemble_score differs from rule_value by more than threshold.

        Parameters:
        -----------
        ens_label : str
            Ensemble-derived label.
        rule_label : str
            Rating-based label.
        ens_score : float
            Ensemble numeric score.
        threshold : float
            Minimum difference to flag (default 0.5).

        Returns:
        --------
        bool: True if flagged, else False.
        """
        # Map labels to numeric targets
        rule_val = {"positive": +1, "neutral": 0, "negative": -1}[rule_label]
        # Flag if labels differ AND magnitude of mismatch > threshold
        return ens_label != rule_label and abs(ens_score - rule_val) > threshold

    def run(
        self, df: pd.DataFrame, text_col: str = "normalized_review"
    ) -> pd.DataFrame:
        """
        Process a DataFrame of reviews, adding sentiment fields and flags.

        Parameters:
        -----------
        df : pd.DataFrame
            Input with at least columns [text_col, 'rating'].
        text_col : str
            Column name containing review text to score.

        Returns:
        --------
        pd.DataFrame
            Original DataFrame augmented with:
              ['bert','vader','textblob','ensemble','label',
               'uncertainty','rule_label','flag']
        """
        # Defensive check: required columns
        if text_col not in df.columns or "rating" not in df.columns:
            raise KeyError(f"Required columns missing: '{text_col}' and/or 'rating'")

        # List to collect new sentiment records
        records = []
        # Iterate rows
        for _, row in df.iterrows():
            text = str(row[text_col])  # Ensure string
            rating = int(row["rating"])  # Ensure int
            rec = self.compute_ensemble(text)  # Compute scores
            rec["rule_label"] = self.apply_rating_rule(rec["label"], rating)
            rec["flag"] = self.flag_disagreement(
                rec["label"], rec["rule_label"], rec["ensemble"]
            )
            records.append(rec)  # Append record

        # Build DataFrame of sentiment results
        sent_df = pd.DataFrame(records, index=df.index)
        # Concatenate original + sentiment results
        return pd.concat(
            [df.reset_index(drop=True), sent_df.reset_index(drop=True)], axis=1
        )
