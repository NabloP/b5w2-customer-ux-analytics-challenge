"""
test_data_loader.py – Unit Tests for DataLoader Class (B5W2)
------------------------------------------------------------

Tests functionality of the DataLoader class from theme_data_loader.py,
including:
- File loading and schema validation
- Malformed theme parsing
- Defensive behavior on invalid or missing input

Author: Nabil Mohamed
"""

import os  # OS-level utilities for path handling
import sys  # Needed to modify the Python path
from pathlib import Path  # Safer file path resolution

# Get the absolute path to the root of the project (one level up from /tests)
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))  # Prepend root to import src modules

# ───────────────────────────────────────────────────────────────────────────────
# 📦 Imports – Standard, Third-Party, and Local
# ───────────────────────────────────────────────────────────────────────────────

from pathlib import Path  # ✅ Cross-platform fixture resolution
import pytest  # ✅ Pytest test framework
import pandas as pd  # ✅ DataFrame checks

from src.visualization.theme_data_loader import DataLoader  # 🔍 Class under test

# ───────────────────────────────────────────────────────────────────────────────
# 🧪 Test 1 – Ensure All Fixture Files Exist
# ───────────────────────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "filename",
    [
        "valid_data.csv",
        "missing_column_data.csv",  # has 'date' but intentionally missing 'themes'
        "malformed_data.csv",
        "malformed_themes_data.csv",
        "theme_metrics_data.csv",
    ],
)
def test_fixture_exists(filename):
    """✅ Ensure all required test fixture files are present in /fixtures/."""
    path = Path(__file__).parent / "fixtures" / filename
    assert path.exists(), f"❌ Missing fixture: {filename}"


# ───────────────────────────────────────────────────────────────────────────────
# 🧪 Test 2 – Load Valid Data
# ───────────────────────────────────────────────────────────────────────────────


def test_valid_data_loads_correctly():
    """✅ Should load and parse the valid_data.csv file."""
    path = Path(__file__).parent / "fixtures" / "valid_data.csv"
    loader = DataLoader(str(path))
    df = loader.load()
    assert isinstance(df, pd.DataFrame)
    assert "themes" in df.columns
    assert all(isinstance(x, list) for x in df["themes"].dropna())


# ───────────────────────────────────────────────────────────────────────────────
# 🧪 Test 3 – Defensive Error Handling
# ───────────────────────────────────────────────────────────────────────────────


def test_file_not_found_raises():
    """❌ Should raise FileNotFoundError if path does not exist."""
    path = Path("fixtures") / "nonexistent_file.csv"
    with pytest.raises(FileNotFoundError):
        DataLoader(str(path))


def test_non_string_path_raises():
    """❌ Should raise TypeError if path is not a string."""
    with pytest.raises(TypeError):
        DataLoader(123)


def test_missing_required_columns():
    """❌ Should raise ValueError if 'themes' column is missing."""
    path = Path(__file__).parent / "fixtures" / "missing_column_data.csv"
    loader = DataLoader(str(path))
    with pytest.raises(ValueError) as exc:
        loader.load()
    assert "themes" in str(exc.value)


# ───────────────────────────────────────────────────────────────────────────────
# 🧪 Test 4 – Malformed Theme Parsing
# ───────────────────────────────────────────────────────────────────────────────


def test_malformed_themes_are_handled():
    """✅ Malformed 'themes' should fallback to list-wrapped strings."""
    path = Path(__file__).parent / "fixtures" / "malformed_themes_data.csv"
    loader = DataLoader(str(path))
    df = loader.load()

    # Check all themes are now lists (even malformed ones)
    assert isinstance(df, pd.DataFrame)
    assert "themes" in df.columns
    # Ensure all non-null theme entries are lists
    non_lists = [x for x in df["themes"].dropna() if not isinstance(x, list)]
    assert not non_lists, f"❌ Found non-list entries in 'themes': {non_lists}"


def test_malformed_rows_are_still_loaded():
    """✅ Even malformed rows should be returned, not silently dropped."""
    path = Path(__file__).parent / "fixtures" / "malformed_data.csv"
    loader = DataLoader(str(path))
    df = loader.load()
    assert not df.empty
