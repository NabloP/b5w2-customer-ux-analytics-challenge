# src/visualization/theme_data_loader.py

"""
theme_data_loader.py – Thematic UX Review Data Loader (B5W2)
----------------------------------------------------------------------
Safely loads the enriched review dataset with sentiment and theme labels
for visualization and diagnostic analysis.

Core responsibilities:
  • Validates CSV structure and required columns
  • Parses the 'themes' column from string → list using literal_eval
  • Handles malformed or missing theme rows gracefully

Required columns:
  ['review', 'rating', 'ensemble', 'bank', 'themes', 'date']

Used in all Task 4 visualizations and downstream analysis modules.

Author: Nabil Mohamed
"""


# ───────────────────────────────────────────────────────────────────────────────
# 📦 Standard Library Imports
# ───────────────────────────────────────────────────────────────────────────────
import os  # For file path validation
import ast  # For safe string-to-list conversion

# ───────────────────────────────────────────────────────────────────────────────
# 📦 Third-Party Imports
# ───────────────────────────────────────────────────────────────────────────────
import pandas as pd  # For DataFrame operations


# ───────────────────────────────────────────────────────────────────────────────
# 🧠 Class: DataLoader
# ───────────────────────────────────────────────────────────────────────────────
class DataLoader:
    """
    OOP wrapper to load a cleaned review dataset and ensure its 'themes' column is parsed as a Python list.
    Validates the file path, structure, and column presence.
    """

    def __init__(self, filepath: str):
        """
        Initialize the loader with the path to a CSV file.
        Validates file existence and input type.

        Args:
            filepath (str): Path to the CSV file to load.

        Raises:
            TypeError: If filepath is not a string.
            FileNotFoundError: If file does not exist at the given path.
        """
        # 🛡️ Ensure the input path is a string
        if not isinstance(filepath, str):
            raise TypeError(f"filepath must be str, got {type(filepath)}")

        # 🛡️ Check whether the file exists
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"Cannot find file at {filepath}")

        # ✅ Save filepath for later use
        self.filepath = filepath

    def load(self) -> pd.DataFrame:
        """
        Load and return the cleaned DataFrame, with 'themes' parsed into Python lists.

        Returns:
            pd.DataFrame: Cleaned and validated DataFrame with 'themes' parsed.

        Raises:
            ValueError: If required columns are missing.
        """
        # 🧾 Read the CSV into a DataFrame
        df = pd.read_csv(self.filepath)

        # ✅ Define required columns for validation
        required = {"review", "rating", "ensemble", "bank", "themes", "date"}

        # ❌ Identify any missing columns
        missing = required.difference(df.columns)
        if missing:
            raise ValueError(f"Missing columns in data: {missing}")

        # 🔄 Parse the 'themes' column into list format using helper
        df["themes"] = df["themes"].apply(self._parse_themes)

        # ✅ Return the cleaned DataFrame
        return df

    @staticmethod
    def _parse_themes(cell):
        """
        Convert a string literal like "['A','B']" into a Python list.
        Gracefully fallback if the string is malformed or non-list-like.

        Args:
            cell (Any): The raw value from the 'themes' column.

        Returns:
            list | original: Parsed list or original/fallback value.
        """
        # ✅ If the cell is already a list, return it unchanged
        if isinstance(cell, list):
            return cell

        # ✅ If the cell is a string, try to safely evaluate it
        if isinstance(cell, str):
            try:
                # 🧠 Use literal_eval to parse legitimate list-like strings
                parsed = ast.literal_eval(cell)

                # ✅ If parsed result is a list, return as-is
                if isinstance(parsed, list):
                    return parsed

                # ⚠️ If it's not a list (e.g., single string or dict), wrap it
                return [parsed]

            except (ValueError, SyntaxError):
                # ❌ Fallback: treat entire malformed string as a single theme
                return [cell]

        # 🔁 For anything else (e.g., NaN, None), return as-is
        return cell
