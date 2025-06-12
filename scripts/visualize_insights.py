"""
visualize_insights.py – Insight Visualization Runner for Customer UX (B5W2)
----------------------------------------------------------------------------

Generates 7 key visualizations from enriched app reviews for CBE, BOA, and Dashen,
using modular components to surface theme-level, sentiment-level, and UX-level signals.

Features:
- Loads enriched dataset with theme-labeled reviews
- Renders all 7 plots inline (rating dist, sentiment trend, heatmaps, clouds, etc.)
- Supports parameterized comparison for bubble chart theme
- Modular and OOP-aligned for reproducibility

Author: Nabil Mohamed
"""

# ───────────────────────────────────────────────────────────────────────────────
# 🧠 Visualize Task 4 Insights – Full Plotting Orchestrator
# ───────────────────────────────────────────────────────────────────────────────

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
expected_path = "src/visualization"
print(
    "📁 Visualization module path ready"
    if os.path.exists(expected_path)
    else f"⚠️ Visualization module path not found: {expected_path}"
)
# ------------------------------------------------------------------------------

# 1️⃣ Standard Imports
import warnings  # suppress any pandas warnings for cleaner UX

# 2️⃣ Local Module Imports (via src structure)
from src.visualization.theme_data_loader import DataLoader
from src.visualization.plot_generator import PlotGenerator

# 3️⃣ Suppress pandas SettingWithCopyWarnings (optional)
warnings.simplefilter(action="ignore", category=FutureWarning)

# 4️⃣ Configurable Parameters
CSV_PATH = "data/outputs/reviews_with_sentiment_themes.csv"  # ✅ Your enriched dataset
BANKS = ["CBE", "BOA", "Dashen"]  # ✅ The 3 target banks
KEY_THEME = "Functionality"  # 💡 Customize this for the bubble chart

# 5️⃣ Load the DataFrame
loader = DataLoader(filepath=CSV_PATH)  # 🧹 Handles parsing + validation
df = loader.load()  # 🧼 Cleaned, theme-parsed DataFrame ready for plotting

# 6️⃣ Initialize Plot Generator
plotter = PlotGenerator(df)  # 🎨 Unified access to all 7 plot types

# 7️⃣ Sequentially Run All Visualizations
print("📊 Plotting Rating Distributions...")
plotter.plot_rating_distribution(banks=BANKS)

print("📈 Plotting Sentiment Trends...")
plotter.plot_sentiment_trends()

print("🌡️ Plotting Theme vs. Rating Heatmap...")
plotter.plot_theme_rating_heatmap(banks=BANKS)

print("🔥 Plotting Complaint Frequency Heatmap (Negative Sentiment)...")
plotter.plot_negative_complaint_heatmap()

print("☁️ Generating Word Clouds per Bank...")
plotter.plot_word_clouds()

print("🛠️ Plotting Feature Request Bar Chart (Negative Sentiment)...")
plotter.plot_negative_feature_requests(
    candidate_themes=["Feature Requests", "Functionality", "UI/UX", "Notifications"]
)

print(f"💎 Plotting Bubble Chart for Key Theme: {KEY_THEME}")
plotter.plot_bubble_chart(key_theme=KEY_THEME, banks=BANKS)

print("✅ All plots rendered inline successfully.")
