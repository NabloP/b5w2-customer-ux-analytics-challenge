"""
scraping_runner.py – Batch Scraper Execution Script (B5W2)
-----------------------------------------------------------

Script to scrape user reviews from the Google Play Store for three Ethiopian banks.
Aggregates all reviews into a single CSV export for downstream sentiment and theme analysis.

Features:
- Ensures consistent working directory for `src/` imports
- Loops through all bank app IDs using the modular BankReviewScraper class
- Combines all reviews into a clean CSV with the required schema

Author: Nabil Mohamed
"""

# ------------------------------------------------------------------------------
# 🛠 Ensure Script Runs from Project Root (for src/ imports to work)
# ------------------------------------------------------------------------------

import os
import sys

# If running from /notebooks/, move up to project root
if os.path.basename(os.getcwd()) == "notebooks":
    os.chdir("..")
    print("📂 Changed working directory to project root")

# Add project root to sys.path so `src/` modules can be imported
project_root = os.getcwd()
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"✅ Added to sys.path: {project_root}")

# Confirm expected output path
expected_path = "data/raw"
print(
    "📁 Output path ready"
    if os.path.exists(expected_path)
    else f"⚠️ Output path not found: {expected_path}"
)


# ------------------------------------------------------------------------------
# 🔁 Task 1 – Batch Scraping & Combined Export for All Banks
# ------------------------------------------------------------------------------

from src.scraper.review_scraper import BankReviewScraper
import pandas as pd

# 📌 Define bank metadata (Play Store app IDs)
BANKS = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking",
    "Dashen": "com.dashen.dashensuperapp",
}

# ⚙️ Scraping configuration
REVIEW_TARGET = 400  # Reviews per bank
OUTPUT_DIR = "data/raw"  # Folder for CSV exports
COMBINED_FILENAME = "reviews_all_banks.csv"  # Combined output file
OUTPUT_PATH = os.path.join(OUTPUT_DIR, COMBINED_FILENAME)

# ✅ Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 📦 Initialize list to collect all bank reviews
all_reviews = []

# 🔁 Loop through banks and scrape reviews
for bank_label, app_id in BANKS.items():
    print(f"\n🚀 Scraping {REVIEW_TARGET} reviews for {bank_label}...")

    try:
        # Initialize scraper instance
        scraper = BankReviewScraper(
            app_id=app_id,
            bank_label=bank_label,
            target_count=REVIEW_TARGET,
            verbose=True,
        )

        # Run scraping pipeline
        scraper.scrape_reviews()

        # Append structured reviews to global list
        all_reviews.extend(scraper.reviews_raw)

        # Optional: save per-bank CSVs for diagnostics
        # bank_csv_path = os.path.join(OUTPUT_DIR, f"reviews_{bank_label}.csv")
        # pd.DataFrame(scraper.reviews_raw).to_csv(bank_csv_path, index=False, encoding="utf-8-sig")

    except Exception as e:
        print(f"❌ Error scraping {bank_label}: {e}")

# 📤 Final combined export
if all_reviews:
    df_all = pd.DataFrame(all_reviews)
    df_all.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"\n✅ Exported {len(df_all):,} combined reviews to: {OUTPUT_PATH}")
else:
    print("⚠️ No reviews collected across all banks.")
