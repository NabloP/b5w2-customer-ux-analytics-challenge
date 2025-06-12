"""
sentiment_pipeline.py – Sentiment + Theme Extraction Pipeline (B5W2)
---------------------------------------------------------------------

Runs full sentiment and theme enrichment on cleaned Google Play Store reviews
for CBE, BOA, and Dashen. Outputs enriched reviews with:

- Ensemble sentiment scores (VADER, TextBlob, DistilBERT)
- Uncertainty metrics and rule-based flags
- Thematic tags from rule-based keyword matching
- Final export: `reviews_with_sentiment_themes.csv`

Author: Nabil Mohamed
"""

# ------------------------------------------------------------------------------
# 🛠 Ensure Script Runs from Project Root (for src/ imports to work)
# ------------------------------------------------------------------------------

import os  # OS utilities for path management
import sys  # Path injection for src imports

# Auto-detect if launched from /notebooks and normalize to project root
if os.path.basename(os.getcwd()) == "notebooks":
    os.chdir("..")
    print("📂 Changed working directory to project root")

# Register root in sys.path
project_root = os.getcwd()
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"✅ Added to sys.path: {project_root}")

# Confirm key data folders are in place
expected_input = "data/cleaned"
expected_output = "data/outputs"
for path in [expected_input, expected_output]:
    print(f"📁 Found: {path}" if os.path.exists(path) else f"⚠️ Missing: {path}")

# ------------------------------------------------------------------------------
# 📥 Load Cleaned Reviews from Disk
# ------------------------------------------------------------------------------

from src.nlp.review_loader import ReviewDataLoader
import pandas as pd

INPUT_PATH = "data/cleaned/reviews_all_banks_cleaned.csv"

try:
    loader = ReviewDataLoader(path=INPUT_PATH, verbose=True)
    df_reviews = loader.load()
    print(f"✅ Loaded {len(df_reviews):,} cleaned reviews")
except Exception as e:
    print(f"❌ Failed to load cleaned reviews: {e}")
    sys.exit(1)

# ------------------------------------------------------------------------------
# 🔄 Normalize Text using SymSpell + spaCy
# ------------------------------------------------------------------------------

from src.nlp.text_normalizer import TextNormalizer

try:
    normalizer = TextNormalizer(use_symspell=True, use_spacy=True)
    print("🔧 TextNormalizer initialized")
except Exception as e:
    print(f"❌ Failed to initialize TextNormalizer: {e}")
    sys.exit(1)

# Determine source text column
source_col = None
if "corrected_review" in df_reviews.columns:
    source_col = "corrected_review"
elif "review" in df_reviews.columns:
    source_col = "review"
else:
    print("❌ No valid text column found in df_reviews")
    sys.exit(1)

print(f"ℹ️ Using column `{source_col}` for normalization")

# Apply normalization row-wise
normalized = []
for i, text in enumerate(df_reviews[source_col].astype(str), start=1):
    try:
        normalized.append(normalizer.normalize(text))
    except Exception as err:
        print(f"⚠️ Error at row {i}: {err}")
        normalized.append("")
    if i % 500 == 0:
        print(f"⏱️ Processed {i:,} reviews")

df_reviews["normalized_review"] = normalized
print(f"✅ Normalized {len(df_reviews):,} reviews")

# ------------------------------------------------------------------------------
# 🤖 Run Sentiment Ensemble (DistilBERT + VADER + TextBlob)
# ------------------------------------------------------------------------------

from src.nlp.sentiment_classifier import SentimentEnsembler

MODEL_DIR = "models/distilbert-base-uncased-finetuned-sst-2-english"

try:
    ensembler = SentimentEnsembler(model_path=MODEL_DIR, device="cpu")
    ensembler.tokenizer = ensembler.tokenizer.from_pretrained(
        MODEL_DIR, local_files_only=True
    )
    ensembler.model = ensembler.model.from_pretrained(
        MODEL_DIR, local_files_only=True
    ).to(ensembler.device)
    print("🔧 Loaded DistilBERT model")
except Exception as e:
    print(f"❌ Sentiment model load failed: {e}")
    sys.exit(1)

df_enriched = ensembler.run(df_reviews, text_col="normalized_review")
print(f"✅ Sentiment enrichment complete ({len(df_enriched):,} rows)")

# ------------------------------------------------------------------------------
# 🧠 Apply Theme Tagging via Rule-Based Keyword Matching
# ------------------------------------------------------------------------------

from src.nlp.keyword_theme_extractor import ThemeExtractor
from src.nlp.stopwords import COMBINED_STOPWORDS

# Define bank-specific seed keywords
seed_map = {
    bank: {
        "Concise Feedback": ["good", "bad", "fine", "ok"],
        "Account Access": ["login", "otp", "password", "pin"],
        "Connection Issues": ["network", "offline", "timeout", "disconnect"],
        "Usability": ["hard to use", "navigate", "layout", "ux"],
        "Performance": ["slow", "lag", "speed", "delay", "fast"],
        "Functionality": ["feature", "cannot", "unable", "doesn't", "option"],
        "Feature Requests": ["should have", "wish", "add", "feature request"],
        "Security & Trust": ["secure", "fraud", "trust", "encryption", "leak"],
        "Notifications": ["alert", "notification", "push", "reminder", "email"],
        "Stability & Bugs": ["crash", "freeze", "error", "bug", "exception"],
    }
    for bank in ["CBE", "BOA", "Dashen"]
}

# Run tagger
try:
    theme_extractor = ThemeExtractor(seed_map=seed_map)
    df_tagged = theme_extractor.tag_corpus(df_enriched)
    print("🏷️  Theme tagging complete")
except Exception as e:
    print(f"❌ Theme extraction failed: {e}")
    sys.exit(1)

# ------------------------------------------------------------------------------
# 💾 Export Enriched Data for Visualization
# ------------------------------------------------------------------------------

OUTPUT_PATH = "data/outputs/reviews_with_sentiment_themes.csv"

try:
    df_tagged.to_csv(OUTPUT_PATH, index=False)
    print(f"\n✅ Pipeline complete! Exported to: {OUTPUT_PATH}")
    print(f"📊 Final row count: {len(df_tagged):,}")
except Exception as e:
    print(f"❌ Failed to export output: {e}")
