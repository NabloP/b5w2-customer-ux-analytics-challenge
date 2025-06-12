"""
test_theme_metrics.py – Unit Tests for ThemeMetricsCalculator (B5W2)
---------------------------------------------------------------------

Tests functionality of the ThemeMetricsCalculator class, including:
- Correct instantiation with valid DataFrame
- Error handling on invalid input types
- Metric computation for valid banks
- Defensive behavior for nonexistent banks

Author: Nabil Mohamed
"""

# ───────────────────────────────────────────────────────────────────────────────
# 📦 Imports – Standard, Third-Party, and Local
# ───────────────────────────────────────────────────────────────────────────────

from pathlib import Path  # Robust file handling
import pytest  # Pytest test framework
import pandas as pd  # For DataFrame operations

# Add project root to sys.path only if needed (usually safe without this)
import sys

project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.visualization.theme_metrics import ThemeMetricsCalculator  # Class under test

# ───────────────────────────────────────────────────────────────────────────────
# 🔧 Fixture – Load test DataFrame once per module
# ───────────────────────────────────────────────────────────────────────────────


@pytest.fixture(scope="module")
def sample_df():
    """Loads the fixture CSV into a DataFrame."""
    fixture_path = Path(__file__).parent / "fixtures" / "theme_metrics_data.csv"
    if not fixture_path.exists():
        raise FileNotFoundError(f"❌ Could not find test fixture at: {fixture_path}")
    return pd.read_csv(fixture_path)


# ───────────────────────────────────────────────────────────────────────────────
# ✅ Test Cases for ThemeMetricsCalculator
# ───────────────────────────────────────────────────────────────────────────────


def test_valid_instantiation(sample_df):
    """✅ Should instantiate correctly with a valid DataFrame."""
    calc = ThemeMetricsCalculator(sample_df)
    assert isinstance(calc, ThemeMetricsCalculator)


def test_invalid_instantiation_type():
    """❌ Should raise TypeError if passed non-DataFrame input."""
    with pytest.raises(TypeError):
        ThemeMetricsCalculator("not_a_dataframe")


def test_missing_columns_in_dataframe(sample_df):
    """❌ Should raise ValueError if required columns are missing."""
    broken = sample_df.drop(columns=["bank"])
    with pytest.raises(ValueError):
        ThemeMetricsCalculator(broken)


def test_compute_metrics_valid_bank(sample_df):
    """✅ Should return valid DataFrame with expected columns for 'CBE'."""
    calc = ThemeMetricsCalculator(sample_df)
    result = calc.compute_for_bank("CBE")
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert {
        "themes",
        "mentions",
        "avg_sentiment",
        "avg_rating",
        "composite_score",
    }.issubset(result.columns)


def test_invalid_bank_type(sample_df):
    """❌ Should raise TypeError for non-string bank input."""
    calc = ThemeMetricsCalculator(sample_df)
    with pytest.raises(TypeError):
        calc.compute_for_bank(123)


def test_nonexistent_bank(sample_df):
    """❌ Should raise ValueError if the bank doesn't exist in dataset."""
    calc = ThemeMetricsCalculator(sample_df)
    with pytest.raises(ValueError):
        calc.compute_for_bank("ZebraBank")
