"""
review_scraper.py – Modular Review Scraper for Google Play (B5W2)
------------------------------------------------------------------

OOP-aligned, defensively programmed module for extracting and exporting
Google Play Store reviews for fintech mobile apps (CBE, BOA, Dashen).

Supports:
- Automated pagination via continuation tokens
- Full-field structured review extraction
- Challenge-compliant CSV exports (5 essential columns)
- Verbose diagnostics for batch scraping workflows

Required output schema (CSV):
    review, rating, date, bank, source

Author: Nabil Mohamed
"""

import os
import time
import pandas as pd
from datetime import datetime
from typing import List, Dict
from google_play_scraper import reviews, Sort


# ------------------------------------------------------------------------------
# 🏦 BankReviewScraper – Modular review collector for a single banking app
# ------------------------------------------------------------------------------


class BankReviewScraper:
    """
    Scrapes and structures Google Play reviews for a specific mobile banking app.

    Attributes:
    -----------
    app_id : str
        The Play Store app ID (e.g., 'com.combanketh.mobilebanking').
    bank_label : str
        A short name to associate with this app (e.g., 'CBE').
    target_count : int
        Number of reviews to retrieve (default: 400).
    verbose : bool
        Whether to print progress logs.
    reviews_raw : List[Dict]
        Internal buffer of fully structured review dicts.
    """

    REQUIRED_FIELDS = ["review", "rating", "date", "bank", "source"]

    def __init__(
        self,
        app_id: str,
        bank_label: str,
        target_count: int = 400,
        verbose: bool = True,
    ):
        self.app_id = app_id
        self.bank_label = bank_label
        self.target_count = target_count
        self.verbose = verbose
        self.reviews_raw: List[Dict] = []

    def scrape_reviews(self) -> None:
        """
        Scrapes reviews from the Google Play Store using continuation tokens.

        Populates:
        ----------
        self.reviews_raw : with full metadata extracted and normalized.

        Raises:
        -------
        RuntimeError : If scraping fails or no reviews are returned.
        """
        collected = []
        token = None

        if self.verbose:
            print(
                f"🔍 Starting scrape for {self.bank_label} ({self.target_count} reviews)..."
            )

        while len(collected) < self.target_count:
            try:
                batch, token = reviews(
                    self.app_id,
                    lang="en",
                    country="us",
                    sort=Sort.NEWEST,
                    count=min(200, self.target_count - len(collected)),
                    filter_score_with=None,
                    continuation_token=token,
                )
            except Exception as e:
                raise RuntimeError(f"❌ Failed to fetch reviews: {e}")

            if not batch:
                break

            collected.extend(batch)

            if self.verbose:
                print(f"📦 Collected {len(collected)} / {self.target_count}")

            if token is None:
                break  # End of pagination

            time.sleep(1)  # Respectful throttle

        if not collected:
            raise RuntimeError(f"🚫 No reviews found for app: {self.bank_label}")

        self.reviews_raw = self._format_full_reviews(collected)

    def _format_full_reviews(self, raw: List[Dict]) -> List[Dict]:
        """
        Maps raw Google Play review fields into structured dictionaries.

        Parameters:
        -----------
        raw : List[Dict]
            List of unstructured review records from `google-play-scraper`.

        Returns:
        --------
        List[Dict] : Structured reviews with full metadata.
        """
        formatted = []
        for r in raw:
            formatted.append(
                {
                    "review": r.get("content", "").strip(),
                    "rating": r.get("score"),
                    "date": r.get("at").strftime("%Y-%m-%d") if r.get("at") else None,
                    "bank": self.bank_label,
                    "source": "Google Play",
                    "reviewId": r.get("reviewId"),
                    "userName": r.get("userName"),
                    "userImage": r.get("userImage"),
                    "appVersion": r.get("appVersion"),
                    "repliedAt": r.get("repliedAt"),
                    "replyContent": r.get("replyContent"),
                    "thumbsUpCount": r.get("thumbsUpCount"),
                }
            )
        return formatted

    def export_to_csv(self, output_path: str) -> None:
        """
        Exports the scraped reviews to a CSV file using the required output schema.

        Parameters:
        -----------
        output_path : str
            Destination path for the CSV (e.g., 'data/cleaned/reviews_CBE.csv').

        Raises:
        -------
        ValueError : If scraping hasn't been run yet or output fails.
        """
        if not self.reviews_raw:
            raise ValueError("⚠️ No reviews available. Run `scrape_reviews()` first.")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        df = pd.DataFrame(self.reviews_raw)

        try:
            df_required = df[self.REQUIRED_FIELDS]
        except KeyError as e:
            raise ValueError(f"❌ Export failed – missing expected fields: {e}")

        df_required.to_csv(output_path, index=False, encoding="utf-8-sig")

        if self.verbose:
            print(f"✅ Exported {len(df_required):,} reviews to {output_path}")
