# src/nlp/text_normalizer.py

"""
text_normalizer.py – Text Normalization Module (B5W2)
------------------------------------------------------
Provides basic cleaning, spelling correction, and lemmatization
for user reviews. Designed as Tier 1 in a multi-tier fallback
pipeline (with placeholders for GECToR and LLM-based correction).

Responsibilities:
- Remove unwanted characters & URLs
- Collapse whitespace, lowercase text
- Correct spelling via SymSpell
- Lemmatize & remove stopwords via spaCy
- Expose a single .normalize(text) method

Author: Nabil Mohamed
"""

import re  # Regex operations
import spacy  # SpaCy for lemmatization and stopwords
from symspellpy.symspellpy import SymSpell, Verbosity  # SymSpell spell-corrector
import pkg_resources  # To locate symspell dictionaries
from typing import Optional  # Type hinting for readability


class TextNormalizer:
    """
    A modular text normalizer for cleaning and standardizing review text.
    Tier 1: Uses rule-based and statistical methods only (no LLM).
    """

    def __init__(
        self,
        use_symspell: bool = True,
        use_spacy: bool = True,
        max_edit_distance: int = 2,
        prefix_length: int = 7,
    ):
        """
        Initialize the normalizer, loading SymSpell and spaCy if enabled.

        Parameters:
        -----------
        use_symspell : bool
            Whether to perform spelling correction.
        use_spacy : bool
            Whether to perform lemmatization & stopword removal.
        max_edit_distance : int
            Max edit distance for SymSpell suggestions.
        prefix_length : int
            Prefix length for SymSpell’s dictionary.
        """
        # Toggle spell correction
        self.use_symspell = use_symspell
        # Toggle linguistic normalization
        self.use_spacy = use_spacy
        # Placeholder for SymSpell instance
        self.symspell: Optional[SymSpell] = None
        # Placeholder for SpaCy NLP pipeline
        self.nlp = None

        # Initialize SymSpell if requested
        if self.use_symspell:
            self.symspell = SymSpell(
                max_dictionary_edit_distance=max_edit_distance,
                prefix_length=prefix_length,
            )
            # Load frequency and bigram dictionaries
            dict_path = pkg_resources.resource_filename(
                "symspellpy", "frequency_dictionary_en_82_765.txt"
            )
            bigram_path = pkg_resources.resource_filename(
                "symspellpy", "frequency_bigramdictionary_en_243_342.txt"
            )
            # Defensive loading
            if not self.symspell.load_dictionary(
                dict_path, term_index=0, count_index=1
            ):
                raise FileNotFoundError(f"SymSpell dictionary not found at {dict_path}")
            if not self.symspell.load_bigram_dictionary(
                bigram_path, term_index=0, count_index=2
            ):
                raise FileNotFoundError(
                    f"SymSpell bigram dict not found at {bigram_path}"
                )

        # Initialize spaCy if requested
        if self.use_spacy:
            try:
                self.nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
            except OSError as e:
                raise OSError(
                    "spaCy model 'en_core_web_sm' not found. "
                    "Run `python -m spacy download en_core_web_sm`."
                ) from e

    def _basic_clean(self, text: str) -> str:
        """
        Perform regex-based cleaning:
        - Remove URLs
        - Strip non-alphanumeric (except basic punctuation)
        - Collapse whitespace
        - Lowercase
        """
        # Ensure string
        txt = str(text)
        # Remove URLs
        txt = re.sub(r"https?://\S+|www\.\S+", " ", txt)
        # Keep letters, numbers, and basic punctuation
        txt = re.sub(r"[^A-Za-z0-9.,!?'\s]", " ", txt)
        # Collapse multiple spaces
        txt = re.sub(r"\s+", " ", txt).strip()
        # Lowercase for uniformity
        return txt.lower()

    def _correct_spelling(self, text: str) -> str:
        """
        Use SymSpell to correct spelling in the text.
        Falls back to original if no suggestions.
        """
        if not self.symspell or not text:
            return text
        # Lookup compound suggestions
        suggestions = self.symspell.lookup_compound(text, max_edit_distance=2)
        # Return best suggestion or original
        return suggestions[0].term if suggestions else text

    def _lemmatize(self, text: str) -> str:
        """
        Lemmatize and remove stopwords via spaCy.
        Returns lemmatized string.
        """
        if not self.nlp or not text:
            return text
        doc = self.nlp(text)
        # Join lemmas of non-stop tokens
        return " ".join(
            token.lemma_ for token in doc if not token.is_stop and token.lemma_.strip()
        )

    def normalize(self, text: str) -> str:
        """
        Full normalization pipeline:
        1. Basic clean
        2. Optional spell correction
        3. Optional lemmatization

        Returns the normalized text.
        """
        # Early exit for non-str or empty
        if not isinstance(text, str) or not text.strip():
            return ""

        # 1. Basic cleaning
        result = self._basic_clean(text)
        # 2. Spell correction
        if self.use_symspell:
            result = self._correct_spelling(result)
        # 3. Lemmatization
        if self.use_spacy:
            result = self._lemmatize(result)

        return result
