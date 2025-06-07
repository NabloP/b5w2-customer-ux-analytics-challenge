"""
cleaning_runner.py – Cleaning Script for Raw Scraped Reviews (B5W2)
--------------------------------------------------------------------

Processes raw Google Play Store review files for CBE, BOA, and Dashen,
applying standardized cleaning to prepare for sentiment and theme analysis.

Features:
- Removes duplicates and missing values
- Standardizes review text formatting
- Tracks how many rows were dropped (% loss KPI)
- Exports a cleaned CSV ready for modeling

Author: Nabil Mohamed
"""

# ------------------------------------------------------------------------------
# 🛠 Ensure Script Runs from Project Root (for src/ imports to work)
# ------------------------------------------------------------------------------

import os  # OS-level utilities for path handling
import sys  # Allows dynamic path resolution for src module imports

# Check if executed from /notebooks and move up if needed
if os.path.basename(os.getcwd()) == "notebooks":
    os.chdir("..")  # Normalize to project root
    print("📂 Changed working directory to project root")

# Capture project root path
project_root = os.getcwd()

# Add root path to sys.path if not already included
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"✅ Added to sys.path: {project_root}")

# Confirm presence of input folder
expected_path = "data/raw"
print(
    "📁 Raw data path ready"
    if os.path.exists(expected_path)
    else f"⚠️ Raw data path not found: {expected_path}"
)

# ------------------------------------------------------------------------------
# 🧹 Task 1 – Clean Raw Reviews and Export Combined CSV
# ------------------------------------------------------------------------------

from src.cleaning.review_cleaner import ReviewDataCleaner
import pandas as pd

# 📂 File path configuration
INPUT_PATH = "data/raw/reviews_all_banks.csv"
OUTPUT_DIR = "data/cleaned"
OUTPUT_FILENAME = "reviews_all_banks_cleaned.csv"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)

# ✅ Ensure export folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 🔁 Run full cleaning pipeline
try:
    # Initialize cleaner with verbose diagnostics
    cleaner = ReviewDataCleaner(raw_path=INPUT_PATH, verbose=True)

    # Load raw dataset from disk
    df_raw = cleaner.load_raw_data()
    raw_count = len(df_raw)  # Original row count for KPI tracking

    # Apply cleaning logic
    df_cleaned = cleaner.clean()
    cleaned_count = len(df_cleaned)

    # Compute % loss for KPI diagnostics
    loss_count = raw_count - cleaned_count
    loss_pct = (loss_count / raw_count) * 100 if raw_count > 0 else 0.0

    # Export final cleaned data
    cleaner.export_cleaned(OUTPUT_PATH)

    # ✅ Print final metrics and file location
    print(f"\n✅ Cleaning complete. Exported to: {OUTPUT_PATH}")
    print(f"📊 Rows before cleaning: {raw_count:,}")
    print(f"🧹 Rows after cleaning : {cleaned_count:,}")
    print(f"📉 Rows dropped        : {loss_count:,} ({loss_pct:.2f}% loss)")

# ❌ Fail-safe error handler for any exceptions in pipeline
except Exception as e:
    print(f"❌ Cleaning pipeline failed: {e}")
