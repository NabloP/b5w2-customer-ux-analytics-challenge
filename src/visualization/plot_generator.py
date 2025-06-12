# src/visualization/plot_generator.py

"""
plot_generator.py – Visualization Engine for UX Insights (B5W2)
----------------------------------------------------------------------
Generates all required charts and heatmaps for Task 4 of the B5W2 project.

Encapsulated in a single class `PlotGenerator`, this module supports:
  • Bar charts of rating distributions by bank
  • Rolling sentiment trends per bank (7-day mean)
  • Heatmaps: Theme vs. Avg Rating and Complaint Frequencies
  • Word clouds per bank with custom stopwords
  • Feature request volume plots for negative sentiment
  • Bubble charts for theme occurrence vs. rating per bank

All methods are OOP-compliant, defensively programmed, and fully annotated.

Expected DataFrame columns:
  ['review', 'rating', 'ensemble', 'bank', 'themes', 'date', 'normalized_review']

Author: Nabil Mohamed
"""


# Standard library imports
import os  # for file path checks
from typing import List, Optional, Set  # for type hints

# Third-party imports
import pandas as pd  # for DataFrame operations
import matplotlib.pyplot as plt  # for plotting
import seaborn as sns  # for enhanced plot styles
from wordcloud import WordCloud, STOPWORDS  # for word cloud generation

# Local application imports
from .theme_metrics import ThemeMetricsCalculator  # compute theme metrics


class PlotGenerator:
    """
    Encapsulates methods to generate the seven key visualizations
    from an enriched, themed reviews DataFrame.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize with a DataFrame of enriched, themed reviews.
        Args:
            df: DataFrame containing at least columns:
                - 'review', 'rating', 'ensemble', 'bank', 'themes', 'date'
        """
        # Defensive check: df must be a DataFrame
        if not isinstance(df, pd.DataFrame):
            raise TypeError(f"Expected DataFrame, got {type(df)}")
        # Defensive check: required columns must exist
        required = {"review", "rating", "ensemble", "bank", "themes", "date"}
        missing = required.difference(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        # Assign validated DataFrame to instance
        self.df = df.copy()

    def plot_rating_distribution(self, banks: List[str]) -> None:
        """
        Plot bar charts of rating distributions for each bank.
        Args:
            banks: List of bank names to include.
        """
        # Set visual style
        sns.set_style("whitegrid")
        # Create a figure with subplots for each bank
        fig, axes = plt.subplots(
            1, len(banks), figsize=(6 * len(banks), 5), sharey=True
        )
        # Loop through axes and bank names simultaneously
        for ax, bank in zip(axes, banks):
            # Filter DataFrame for this bank's ratings
            counts = (
                self.df[self.df["bank"] == bank]["rating"].value_counts().sort_index()
            )
            # Plot bar chart on this axis
            counts.plot(kind="bar", ax=ax, color="#4C72B0", edgecolor="black")
            # Set titles and labels
            ax.set_title(f"{bank} – Rating Distribution")
            ax.set_xlabel("Star Rating")
            ax.set_ylabel("Review Count")
        # Set a super-title for the entire figure
        plt.suptitle("⭐ User Ratings by Bank", fontsize=16, y=1.02)
        # Adjust layout for neatness
        plt.tight_layout()
        # Render the plot
        plt.show()

    def plot_sentiment_trends(
        self,
        date_col: str = "date",
        sentiment_col: str = "ensemble",
        bank_col: str = "bank",
        window: str = "7D",
        min_periods: int = 1,
    ) -> None:
        """
        Plot rolling mean sentiment trends for each bank over time.
        Args:
            date_col: Name of datetime column.
            sentiment_col: Name of sentiment score column.
            bank_col: Name of bank identifier column.
            window: Time window string for rolling, e.g., '7D'.
            min_periods: Minimum non-null observations to compute rolling.
        """
        # Ensure date column is datetime type
        self.df[date_col] = pd.to_datetime(self.df[date_col])
        # Initialize figure
        plt.figure(figsize=(12, 6))
        # Loop through each distinct bank
        for bank in self.df[bank_col].unique():
            # Extract series of sentiment indexed by date
            series = (
                self.df[self.df[bank_col] == bank]
                .set_index(date_col)[sentiment_col]
                .sort_index()
                .rolling(window, min_periods=min_periods)
                .mean()
            )
            # Plot series with label
            series.plot(label=bank)
        # Set titles and axes labels
        plt.title(f"{window} Rolling Sentiment Trend per Bank")
        plt.xlabel("Date")
        plt.ylabel("Mean Sentiment")
        # Add legend and grid
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.5)
        # Adjust layout
        plt.tight_layout()
        # Display
        plt.show()

    def plot_theme_rating_heatmap(self, banks: List[str]) -> None:
        """
        Plot a heatmap of average rating by theme for each bank.
        Args:
            banks: List of bank names to include.
        """
        # Prepare a list to collect per-bank metrics DataFrames
        frames = []
        # Instantiate a ThemeMetricsCalculator with the DataFrame
        calc = ThemeMetricsCalculator(self.df)
        # Loop through each bank to compute metrics
        for bank in banks:
            # Compute theme metrics for this bank
            m = calc.compute_for_bank(bank).copy()
            # Add a column identifying the bank
            m["bank"] = bank
            # Append to frames list
            frames.append(m)
        # Concatenate all per-bank frames into one
        combined = pd.concat(frames, ignore_index=True)
        # Pivot for heatmap: themes as rows, banks as columns, values avg_rating
        pivot = combined.pivot(index="themes", columns="bank", values="avg_rating")
        # Plot heatmap with color center at midpoint 3
        plt.figure(figsize=(10, 6))
        sns.heatmap(
            pivot,
            annot=False,
            fmt=".2f",
            cmap="RdYlGn",
            center=3,
            linewidths=0.5,
            cbar_kws={"label": "Avg Star Rating"},
        )
        # Set labels and title
        plt.title("Average Rating by Theme and Bank")
        plt.xlabel("Bank")
        plt.ylabel("Theme")
        plt.xticks(rotation=0)
        # Tight layout
        plt.tight_layout()
        # Show plot
        plt.show()

    def plot_negative_complaint_heatmap(
        self, sentiment_col: str = "ensemble", threshold: float = 0.0
    ) -> None:
        """
        Plot a heatmap of complaint frequency for negative-sentiment reviews.
        Args:
            sentiment_col: Name of sentiment score column.
            threshold: Cutoff below which sentiment is considered negative.
        """
        # Filter DataFrame for negative-sentiment rows
        neg_df = self.df[self.df[sentiment_col] < threshold].copy()
        # Explode themes into individual rows
        exploded = neg_df.explode("themes")
        # Count occurrences by bank and theme
        counts = exploded.groupby(["bank", "themes"]).size().reset_index(name="count")
        # Pivot to heatmap format
        pivot = counts.pivot(index="themes", columns="bank", values="count").fillna(0)
        # Sort by total complaints descending
        pivot["total"] = pivot.sum(axis=1)
        pivot = pivot.sort_values("total", ascending=False).drop(columns="total")
        # Plot heatmap
        plt.figure(figsize=(10, 6))
        sns.heatmap(
            pivot,
            annot=True,
            fmt="0.0f",
            cmap="Reds",
            linewidths=0.5,
            cbar_kws={"label": "Negative Mentions"},
        )
        # Set labels and title
        plt.title("Complaints by Theme and Bank (Negative Sentiment)")
        plt.xlabel("Bank")
        plt.ylabel("Theme")
        plt.xticks(rotation=0)
        # Tight layout
        plt.tight_layout()
        # Show plot
        plt.show()

    def plot_word_clouds(
        self,
        text_col: str = "normalized_review",
        bank_col: str = "bank",
        additional_stopwords: Optional[Set[str]] = None,
    ) -> None:
        """
        Generate and display word clouds for each bank.
        Args:
            text_col: Column containing text reviews.
            bank_col: Column identifying the bank.
            additional_stopwords: Extra words to exclude.
        """
        # Prepare stopwords set, extending default STOPWORDS
        stopwords = set(STOPWORDS)
        # If user provided extras, add them
        if additional_stopwords:
            stopwords |= additional_stopwords
        # Loop through each unique bank
        for bank in self.df[bank_col].unique():
            # Combine all text into one string
            texts = " ".join(
                self.df[self.df[bank_col] == bank][text_col].dropna().tolist()
            )
            # Initialize WordCloud with given parameters
            wc = WordCloud(
                width=800,
                height=400,
                background_color="white",
                max_words=100,
                stopwords=stopwords,
                colormap="viridis",
            ).generate(texts)
            # Plot the cloud
            plt.figure(figsize=(10, 5))
            plt.imshow(wc, interpolation="bilinear")
            plt.axis("off")
            plt.title(f"Word Cloud for {bank}", fontsize=14)
            plt.tight_layout()
            plt.show()

    def plot_negative_feature_requests(
        self,
        candidate_themes: List[str],
        sentiment_col: str = "ensemble",
        threshold: float = 0.0,
    ) -> None:
        """
        Plot bar chart of negative-sentiment mentions for feature request themes.
        Args:
            candidate_themes: List of themes considered 'feature requests'.
            sentiment_col: Column of sentiment scores.
            threshold: Cutoff below which sentiment is negative.
        """
        # Filter to negative-sentiment reviews
        neg = self.df[self.df[sentiment_col] < threshold]
        # Explode themes
        exploded = neg.explode("themes")
        # Determine which candidate themes actually appear
        valid = [t for t in candidate_themes if t in exploded["themes"].unique()]
        # Filter exploded to only valid feature request themes
        feat = exploded[exploded["themes"].isin(valid)]
        # Count mentions by bank and theme
        counts = feat.groupby(["bank", "themes"]).size().reset_index(name="mentions")
        # Plot bar chart
        plt.figure(figsize=(12, 6))
        sns.barplot(data=counts, x="themes", y="mentions", hue="bank", palette="Set1")
        # Set titles and labels
        plt.title("Negative Feature Requests by Theme and Bank")
        plt.xlabel("Feature Theme")
        plt.ylabel("Negative Mentions")
        plt.xticks(rotation=20)
        plt.legend(title="Bank")
        plt.tight_layout()
        # Show
        plt.show()

    def plot_bubble_chart(self, key_theme: str, banks: List[str]) -> None:
        """
        Plot bubble chart of mentions vs avg_rating for a key theme across banks.
        Args:
            key_theme: The theme to compare.
            banks: List of bank names.
        """
        # Instantiate metrics calculator
        calc = ThemeMetricsCalculator(self.df)
        # Build rows for comparison
        rows = []
        for bank in banks:
            # Compute metrics for this bank
            dfm = calc.compute_for_bank(bank)
            # Filter to the key theme
            rec = dfm[dfm["themes"] == key_theme]
            # Defensive check: ensure the theme exists
            if rec.empty:
                continue
            # Convert the first match to dict and add bank label
            row = rec.iloc[0].to_dict()
            row["bank"] = bank
            rows.append(row)
        # Create DataFrame or raise if no data
        if not rows:
            raise ValueError(f"No data found for theme '{key_theme}'")
        cmp_df = pd.DataFrame(rows)
        # Prepare bubble sizes proportional to mentions
        sizes = (cmp_df["mentions"] / cmp_df["mentions"].max()) * 1000
        # Plot scatter with bubble sizes
        plt.figure(figsize=(8, 6))
        plt.scatter(cmp_df["avg_rating"], cmp_df["mentions"], s=sizes, alpha=0.7)
        # Annotate each point with bank name
        for _, r in cmp_df.iterrows():
            plt.text(
                r["avg_rating"] + 0.02, r["mentions"] + 2, r["bank"], weight="bold"
            )
        # Set titles and labels
        plt.title(f"Occurence vs. Avg Rating for '{key_theme}'", fontsize=14)
        plt.xlabel("Average Star Rating")
        plt.ylabel("Number of Mentions")
        plt.xlim(1, 5)
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        # Show plot
        plt.show()
