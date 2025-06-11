# src/nlp/stopwords.py

"""
stopwords.py – Centralized Stopword Definitions (B5W2)
-------------------------------------------------------
Defines the combined set of English and domain-specific stopwords
for use across all NLP extraction modules.

Author: Nabil Mohamed
"""

import nltk  # for downloading and accessing NLTK data
from nltk.corpus import stopwords  # for the base English stopword list

# Ensure that the NLTK English stopwords resource is available
nltk.download("stopwords", quiet=True)

# Load NLTK's standard English stopwords
NLTK_STOPWORDS = set(stopwords.words("english"))

# Define additional domain-specific terms to exclude from analysis
DOMAIN_STOPWORDS = {
    "bank",
    "app",
    "login",
    "account",
    "service",
    "mobile",
    "platform",
    "application",
    "review",
}

# Combine the two sets into a single master stopword set
COMBINED_STOPWORDS = NLTK_STOPWORDS.union(DOMAIN_STOPWORDS)
