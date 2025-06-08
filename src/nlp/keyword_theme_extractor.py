# src/nlp/keyword_theme_extractor.py

"""
keyword_theme_extractor.py – Keyword, Key Phrase & Theme Extraction Module (B5W2)
-------------------------------------------------------------------------------
Provides three modular classes to:
  a) Extract top-N keywords via TF-IDF
  b) Extract key phrases via spaCy noun chunks
  c) Assign themes based on seed keyword maps

Stopwords are centralized in src/nlp/stopwords.py as COMBINED_STOPWORDS.

Author: Nabil Mohamed
"""

import re  # regex for text cleaning
import spacy  # spaCy for NLP (noun chunks)
from sklearn.feature_extraction.text import TfidfVectorizer  # TF-IDF
from typing import List, Dict  # type hints
from collections import Counter  # counting frequencies

# import centralized stopwords set
from src.nlp.stopwords import COMBINED_STOPWORDS


class KeywordExtractor:
    """
    Extracts top-N TF-IDF keywords (unigrams + bigrams) from a corpus.
    """

    def __init__(
        self,
        stopwords: List[str] = None,  # custom or default stopwords
        max_features: int = 30,  # top N keywords
        ngram_range: tuple = (1, 2),  # use unigrams + bigrams
    ):
        # use provided stopwords or default combined set
        self.stopwords = stopwords or list(COMBINED_STOPWORDS)
        # number of features to extract
        self.max_features = max_features
        # ngram range for TF-IDF
        self.ngram_range = ngram_range
        # placeholder for the fitted TF-IDF vectorizer
        self.vectorizer: TfidfVectorizer = None

    def fit(self, texts: List[str]):
        """
        Fit the TF-IDF vectorizer on the provided list of documents.
        """
        # initialize TF-IDF with custom parameters
        self.vectorizer = TfidfVectorizer(
            stop_words=self.stopwords,  # apply stopwords
            ngram_range=self.ngram_range,  # set ngram range
            max_features=self.max_features,  # limit feature count
        )
        # learn vocabulary and IDF weights
        self.vectorizer.fit(texts)

    def extract_keywords(self, texts: List[str]) -> List[str]:
        """
        Return the top-N keywords from the fitted vectorizer.
        """
        # fit vectorizer if not already done
        if self.vectorizer is None:
            self.fit(texts)
        # return feature names sorted by TF-IDF importance
        return list(self.vectorizer.get_feature_names_out())


class KeyPhraseExtractor:
    """
    Extracts and filters key phrases (noun chunks) from text using spaCy.
    Requires spaCy model with parser enabled for noun_chunks.
    """

    def __init__(
        self,
        spacy_model: str = "en_core_web_sm",  # spaCy model name
        stopwords: List[str] = None,  # custom or default stopwords
    ):
        # load full spaCy pipeline including parser
        self.nlp = spacy.load(spacy_model)
        # use provided stopwords or default combined set
        self.stopwords = set(stopwords or COMBINED_STOPWORDS)

    def extract_phrases(self, text: str) -> List[str]:
        """
        Parse one document and return filtered noun chunks.
        """
        # process text through spaCy NLP pipeline
        doc = self.nlp(text)
        phrases = []  # list to collect noun phrases
        # iterate over each noun chunk in the doc
        for chunk in doc.noun_chunks:
            # normalize to lowercase and strip whitespace
            phrase = chunk.text.lower().strip()
            # remove non-alphanumeric characters
            phrase = re.sub(r"[^a-z0-9\s]", " ", phrase)
            # collapse multiple spaces into one
            phrase = re.sub(r"\s+", " ", phrase).strip()
            # skip empty phrases or those containing stopwords
            if not phrase or any(tok in self.stopwords for tok in phrase.split()):
                continue
            # add the cleaned phrase
            phrases.append(phrase)
        return phrases  # return list of valid phrases

    def extract_top_phrases(self, texts: List[str], top_n: int = 20) -> List[str]:
        """
        Aggregate noun chunks over corpus and return top-N by frequency.
        """
        all_phrases = []  # collect all phrases
        # extract phrases from each document
        for txt in texts:
            all_phrases.extend(self.extract_phrases(txt))
        # count phrase frequencies
        counts = Counter(all_phrases)
        # return the most common top_n phrases
        return [p for p, _ in counts.most_common(top_n)]


class ThemeExtractor:
    """
    Assigns predefined themes to each review based on seed keywords.
    Expanded to include themes like connectivity, usability, performance, etc.
    """

    def __init__(self, seed_map: Dict[str, Dict[str, List[str]]]):
        """
        seed_map: {
          'CBE': {
             'Concise Feedback': ['good','bad','fine','ok'],
             'Account Access':   ['login','otp','password','pin'],
             'Connection Issues':['network','offline','timeout','disconnect'],
             'Usability':        ['hard to use','navigate','layout','ux'],
             'Performance':      ['slow','lag','speed','delay','fast'],
             'Functionality':    ['feature','cannot','unable','doesn't','option'],
             'Feature Requests':['should have','wish','add','feature request'],
             'Security & Trust':['secure','fraud','trust','encryption','leak'],
             'Notifications':    ['alert','notification','push','reminder','email'],
             'Stability & Bugs': ['crash','freeze','error','bug','exception'],
          },
          'BOA': { ... },
          'Dashen': { ... }
        }
        """
        # store per-bank theme keyword mapping
        self.seed_map = seed_map

    def tag_review(self, text: str, bank: str) -> List[str]:
        """
        Return a list of themes matching the text for the given bank.
        """
        # lowercase the text for case-insensitive matching
        text_low = text.lower()
        themes = []  # collect matched themes
        # get the seed keywords for this bank
        bank_seeds = self.seed_map.get(bank, {})
        # iterate through each theme and its keywords
        for theme, keywords in bank_seeds.items():
            for kw in keywords:
                # if keyword appears in the text, tag this theme
                if kw in text_low:
                    themes.append(theme)
                    break  # avoid duplicate theme tags
        # default to "Other" if no themes matched
        return themes or ["Other"]

    def tag_corpus(
        self,
        df,
        text_col: str = "normalized_review",  # column with normalized text
        bank_col: str = "bank",  # column with bank name
    ):
        """
        Apply theme tagging to an entire DataFrame.
        Returns a copy with a new 'themes' column.
        """
        # create a copy to avoid mutating the original
        df_out = df.copy()
        # apply tag_review row-wise to populate themes
        df_out["themes"] = df_out.apply(
            lambda r: self.tag_review(r[text_col], r[bank_col]), axis=1
        )
        return df_out  # return the tagged DataFrame
