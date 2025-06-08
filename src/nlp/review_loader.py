# src/utils/review_loader.py

"""
review_loader.py – Cleaned Reviews Dataset Loader (B5W2)
---------------------------------------------------------

Modular, fault-tolerant loader for cleaned Google Play reviews CSV.
Designed to load 'reviews_all_banks_cleaned.csv' with:
- UTF-8 (fallback to latin1) encoding
- Optional parsing of the 'date' column to datetime
- Verbose diagnostic summaries of shape and columns

Author: Nabil Mohamed
"""

import os
import pandas as pd
from pandas.errors import EmptyDataError, ParserError
from typing import Optional, List


class ReviewDataLoader:
    """
    Loader for cleaned app reviews, with graceful error handling and diagnostics.

    Attributes:
    -----------
    path : str
        Full filesystem path to the cleaned reviews CSV.
    parse_dates : List[str]
        List of columns to parse as datetime (default ['date']).
    verbose : bool
        If True, prints loading diagnostics.
    encoding_used : Optional[str]
        The encoding that succeeded ('utf-8' or 'latin1').
    df : Optional[pd.DataFrame]
        The loaded DataFrame after calling load().
    """

    DEFAULT_DATE_COLUMNS: List[str] = ["date"]  # default datetime columns

    def __init__(
        self,
        path: str = "data/cleaned/reviews_all_banks_cleaned.csv",
        parse_dates: Optional[List[str]] = None,
        verbose: bool = True,
    ):
        # Store the path to the cleaned reviews file
        self.path = path
        # Use provided parse_dates or default to ['date']
        self.parse_dates = parse_dates or self.DEFAULT_DATE_COLUMNS
        # Toggle verbose diagnostics
        self.verbose = verbose
        # Will hold the encoding that worked
        self.encoding_used: Optional[str] = None
        # Placeholder for the loaded DataFrame
        self.df: Optional[pd.DataFrame] = None

    def load(self) -> pd.DataFrame:
        """
        Load the cleaned reviews CSV with UTF-8 (fallback to latin1).
        Parses specified date columns and prints diagnostics if verbose.

        Returns:
        --------
        pd.DataFrame
            The loaded DataFrame with parsed dates.

        Raises:
        -------
        FileNotFoundError
            If the CSV does not exist at self.path.
        ValueError
            If the file is empty or fails parsing.
        """
        # Check that the file exists
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"❌ File not found: {self.path}")

        # Attempt to read with utf-8, fallback to latin1
        try:
            df = self._read_csv(encoding="utf-8")
            self.encoding_used = "utf-8"
        except UnicodeDecodeError:
            df = self._read_csv(encoding="latin1")
            self.encoding_used = "latin1"
            if self.verbose:
                print(f"⚠️ Encoding utf-8 failed; retried with latin1")

        # Check for empty DataFrame
        if df.empty:
            raise ValueError(f"🚫 Loaded DataFrame is empty: {self.path}")

        # Store loaded DataFrame
        self.df = df

        # Print diagnostics if requested
        if self.verbose:
            self._print_summary()

        return df

    def _read_csv(self, encoding: str) -> pd.DataFrame:
        """
        Internal helper to read the CSV file with a specific encoding
        and parse dates.

        Parameters:
        -----------
        encoding : str
            The file encoding to use ('utf-8' or 'latin1').

        Returns:
        --------
        pd.DataFrame
            The DataFrame read from disk.

        Raises:
        -------
        ValueError
            If pandas raises an EmptyDataError or ParserError.
        """
        try:
            return pd.read_csv(
                self.path, parse_dates=self.parse_dates, encoding=encoding
            )
        except (EmptyDataError, ParserError) as e:
            raise ValueError(
                f"❌ Failed to parse CSV ({encoding}): {self.path}\n{e}"
            ) from e

    def _print_summary(self) -> None:
        """
        Print a brief summary of the loaded DataFrame:
        file path, encoding used, number of rows/columns, and column names.
        """
        assert self.df is not None, "DataFrame is not loaded"
        rows, cols = self.df.shape
        print(f"\n📄 File loaded: {self.path}")
        print(f"📦 Encoding used: {self.encoding_used}")
        print(f"🔢 Shape: {rows:,} rows × {cols} columns")
        print(f"🧪 Columns: {', '.join(self.df.columns)}\n")
