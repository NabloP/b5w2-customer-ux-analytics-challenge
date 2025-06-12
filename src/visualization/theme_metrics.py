# src/visualization/theme_metrics.py

"""
theme_metrics.py – Theme-Level UX Metric Calculator (B5W2)
----------------------------------------------------------------------
Provides `ThemeMetricsCalculator`, a class that computes per-theme
metrics for a given bank from an enriched UX dataset.

For a specified bank, it calculates:
  • mentions: how many times each theme appears
  • avg_sentiment: average sentiment score for that theme
  • avg_rating: average user rating associated with that theme
  • composite_score = mentions × avg_sentiment × avg_rating

This class supports theme ranking, complaint diagnostics, and
bubble chart preparation for visualization modules.

Input DataFrame must contain:
  ['review', 'rating', 'ensemble', 'bank', 'themes']

Author: Nabil Mohamed
"""


import pandas as pd  # DataFrame operations


class ThemeMetricsCalculator:
    """
    Encapsulates theme‐level metric computation for a single bank.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Store a reference to the full DataFrame and validate its structure.
        """
        # Defensive programming: ensure df is actually a DataFrame
        if not isinstance(df, pd.DataFrame):
            raise TypeError(f"Expected DataFrame, got {type(df)}")
        # Ensure 'bank' column exists
        if "bank" not in df.columns or "themes" not in df.columns:
            raise ValueError("DataFrame must have 'bank' and 'themes' columns")
        # Save for later use
        self.df = df

    def compute_for_bank(self, bank: str) -> pd.DataFrame:
        """
        Returns a DataFrame of theme metrics for the specified bank.
        Raises if the bank has no rows.
        """
        # Defensive check: bank must be a string
        if not isinstance(bank, str):
            raise TypeError(f"bank must be str, got {type(bank)}")
        # Filter to that bank
        sub = self.df[self.df["bank"] == bank]
        if sub.empty:
            raise ValueError(f"No data found for bank '{bank}'")
        # Explode so each theme is its own row
        exploded = sub.explode("themes")
        # Group and aggregate
        metrics = (
            exploded.groupby("themes")
            .agg(
                mentions=("review", "count"),
                avg_sentiment=("ensemble", "mean"),
                avg_rating=("rating", "mean"),
            )
            .reset_index()
        )
        # Compute composite score
        metrics["composite_score"] = (
            metrics["mentions"] * metrics["avg_sentiment"] * metrics["avg_rating"]
        )
        # Sort by mentions desc for easy inspection
        return metrics.sort_values("mentions", ascending=False)
