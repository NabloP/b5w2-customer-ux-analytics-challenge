"""
review_cleaner.py – Review Data Cleaning Module (B5W2)
------------------------------------------------------

Modular class for cleaning scraped Google Play reviews before analysis.

Responsibilities:
- Load raw review CSVs (saved in `data/raw/`)
- Remove duplicates and null entries in essential fields
- Normalize text fields (e.g., review content)
- Report cleaning diagnostics and export to `data/cleaned/`

Author: Nabil Mohamed
"""

import os
import pandas as pd
from typing import Optional


# ------------------------------------------------------------------------------
# 🧼 ReviewDataCleaner – Cleans raw scraped review CSVs
# ------------------------------------------------------------------------------


class ReviewDataCleaner:
    """
    Class to clean raw Google Play reviews before analysis or modeling.

    Attributes:
    -----------
    raw_path : str
        Path to raw CSV file (e.g., 'data/raw/reviews_all_banks.csv').
    verbose : bool
        Whether to print status logs during cleaning.
    df : pd.DataFrame
        The loaded raw review DataFrame (populated by load_raw_data).
    """

    REQUIRED_COLUMNS = ["review", "rating", "date", "bank", "source"]

    def __init__(self, raw_path: str, verbose: bool = True):
        self.raw_path = raw_path  # Input CSV path (raw review data)
        self.verbose = verbose  # Enable logging if True
        self.df: Optional[pd.DataFrame] = None  # Raw or cleaned DataFrame

    def load_raw_data(self) -> pd.DataFrame:
        """
        Loads the raw CSV file from disk.

        Returns:
        --------
        pd.DataFrame : The raw review dataset.
        """
        if not os.path.exists(self.raw_path):
            raise FileNotFoundError(f"❌ File not found: {self.raw_path}")

        self.df = pd.read_csv(self.raw_path)

        if self.verbose:
            print(
                f"📥 Loaded raw reviews: {self.df.shape[0]:,} rows, {self.df.shape[1]} columns"
            )

        return self.df

    def clean(self) -> pd.DataFrame:
        """
        Cleans the loaded review dataset.

        Operations:
        - Drop rows with nulls in required columns
        - Drop blank review content
        - Drop duplicate reviewIds
        - Normalize whitespace in review text

        Returns:
        --------
        pd.DataFrame : Cleaned DataFrame.
        """
        if self.df is None:
            raise ValueError("⚠️ Data not loaded. Run `load_raw_data()` first.")

        df_clean = self.df.copy()
        total_before = len(df_clean)

        # Drop nulls in required fields
        df_clean.dropna(subset=self.REQUIRED_COLUMNS, inplace=True)
        after_nulls = len(df_clean)
        null_dropped = total_before - after_nulls

        # Drop blank review texts
        df_clean = df_clean[df_clean["review"].str.strip().astype(bool)]
        after_blank = len(df_clean)
        blank_dropped = after_nulls - after_blank

        # Drop duplicate reviewIds
        dup_dropped = 0
        if "reviewId" in df_clean.columns:
            before_dedup = len(df_clean)
            df_clean.drop_duplicates(subset="reviewId", inplace=True)
            dup_dropped = before_dedup - len(df_clean)

        # Normalize whitespace
        df_clean["review"] = (
            df_clean["review"].str.replace(r"\s+", " ", regex=True).str.strip()
        )

        # Summary logging
        total_after = len(df_clean)
        total_dropped = total_before - total_after
        drop_pct = (total_dropped / total_before) * 100 if total_before else 0

        if self.verbose:
            print(f"🧹 Dropped {null_dropped:,} rows with missing fields")
            print(f"🧹 Dropped {blank_dropped:,} rows with blank reviews")
            print(f"🧹 Dropped {dup_dropped:,} duplicate reviewId rows")
            print(
                f"✅ Cleaned dataset has {total_after:,} rows (−{drop_pct:.2f}% loss)"
            )

        self.df = df_clean
        return self.df

    def export_cleaned(self, output_path: str) -> None:
        """
        Exports the cleaned review dataset to a new CSV file.

        Parameters:
        -----------
        output_path : str
            Destination path for the cleaned CSV.
        """
        if self.df is None:
            raise ValueError("⚠️ No cleaned data to export. Run `clean()` first.")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        self.df.to_csv(output_path, index=False, encoding="utf-8-sig")

        if self.verbose:
            print(f"📤 Cleaned reviews exported to: {output_path}")
