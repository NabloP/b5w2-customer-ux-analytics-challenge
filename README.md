# Fintech UX Challenge Week 2 - 10 Academy

## 🗂 Challenge Context
This repository documents the submission for 10 Academy’s **B5W2: Customer Experience Analytics for Fintech Apps** challenge. The objective is to evaluate customer satisfaction with mobile banking apps by scraping, analyzing, and visualizing user reviews from the Google Play Store for:

- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)
- Dashen Bank

This project simulates the role of a data analyst at Omega Consultancy, advising fintechs on improving user experience and retention.

The project includes:

🧹 Clean scraping and preprocessing of Play Store reviews  
💬 Sentiment analysis (VADER, DistilBERT) and keyword clustering  
📊 UX pain point detection and feature insight generation  
🛢️ Relational database setup using Oracle XE  
📈 Stakeholder-ready visualizations and diagnostics


## 🔧 Project Setup

To reproduce this environment:

1. Clone the repository:
   ```bash
git clone https://github.com/NabloP/b5w2-customer-ux-analytics-challenge.git
cd b5w2-customer-ux-analytics-challenge
   ```

2. Create and activate a virtual environment:
   
   **On Windows:**
    ```bash
    python -m venv customer-ux-challenge
    .\customer-ux-challenge\Scripts\Activate.ps1
    ```

    **On macOS/Linux:**
    ```bash
    python3 -m venv customer-ux-challenge
    source customer-ux-challenge/bin/activate
    ```

3. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ CI/CD (GitHub Actions)

This project uses GitHub Actions for Continuous Integration. On every `push` or `pull_request` event, the following workflow is triggered:

- Checkout repo

- Set up Python 3.10

- Install dependencies from `requirements.txt`

CI workflow is defined at:

    `.github/workflows/unittests.yml`

## 📁 Project Structure

<!-- TREE START -->
📁 Project Structure

b5w2-customer-ux-analytics-challenge/
├── data/
│   ├── raw/
│   ├── cleaned/
│   └── outputs/
├── notebooks/
│   ├── task-1-scraping-preprocessing.ipynb
│   ├── task-2-sentiment-thematic-analysis.ipynb
│   ├── task-3-oracle-storage.ipynb
│   └── task-4-insights-visuals.ipynb
├── scripts/
│   ├── scraping_runner.py
│   ├── sentiment_pipeline.py
│   ├── oracle_insert.py
│   ├── visualize_insights.py
├── src/
│   ├── scraper/
│   │   └── review_scraper.py
│   ├── nlp/
│   │   ├── sentiment_classifier.py
│   │   └── keyword_theme_extractor.py
│   ├── db/
│   │   └── oracle_connector.py
│   └── utils/
│       └── preprocessing.py
├── .github/
│   └── workflows/
│       └── unittests.yml
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE


## ✅ Status
- ☑️ Repo initialized and virtual environment created (customer-ux-challenge)
- ☑️ GitHub Actions CI configured for Python 3.10
- ☑️ Play Store scraping functional for 3 bank apps
- ☑️ Review cleaning, deduplication, and date normalization implemented
- ☑️ Sentiment scoring (VADER, DistilBERT) integrated
- ☑️ Keyword extraction and theme clustering per bank working
- ☑️ Oracle database schema + insertion logic tested
- ☑️ Insight visualizations (sentiment bar charts, theme clouds, complaint timelines) generated
- ☑️ Interim report and final report scaffolding prepared


## 📦 What's in This Repo

This repository documents the Week 2 challenge for 10 Academy’s AI Mastery Bootcamp. It includes:

- 📁 **Scaffolded directory structure** using best practices for `src/`, `notebooks/`, `scripts/`, and `tests/`

- 🧪 **CI/CD integration** via GitHub Actions for reproducibility and reliability

- 🧹 **README auto-updating** via `scripts/generate_tree.py` to keep documentation aligned with project layout

- 📚 **Clear Git hygiene** (no committed `.venv` or `.csv`), commit messages and pull request usage

- 🧹 **Data processing pipelines** for scraping, cleaning, sentiment tagging, and keyword-theme extraction using Python and modern NLP libraries (spaCy, TextBlob, Transformers)

- 🧊 **Oracle-compatible database insertion logic**, designed to simulate real-world enterprise data engineering practices in fintech contexts

- 📊 **Visual analytics for stakeholders**, including sentiment distributions, complaint tracking, and keyword clouds

- 🧠 **My Contributions:** All project scaffolding, README setup, automation scripts, and CI configuration were done from scratch by me

## 🧪 Usage

**🔍 How the `eda_orchestrator.py` Pipeline Works**

This script orchestrates the full Task 1 exploratory data analysis (EDA) pipeline for the B5W1 challenge. It covers data loading, text cleaning, sentiment labeling, event extraction, and stock-level headline diagnostics.

📍 Pipeline is intended to be run from the project root. Adjusts automatically if run from `/notebooks/`.

**🔁 Pipeline Steps**

1. Dataset Load

- Loads `raw_analyst_ratings.csv` using a custom loader class.
- Ensures error handling for file not found or format issues.

2. Timestamp Cleaning

- Adds c`leaned_date` by parsing various datetime formats.
- Standardizes timestamps for alignment with OHLCV data.

3. Headline Cleaning

- Applies lowercasing, punctuation removal, HTML stripping, and stopword filtering to headline text.
- Adds `cleaned_headline` column.

4. Feature Extraction

- Computes `word_count` and `headline_length` for textual diagnostics.
- Analyzes top publishers and visualizes their activity by time.

5. Distribution Plots

- Plots histogram distributions of headline lengths and word counts.
- Uses Seaborn styling and verbose labeling for interpretation.

6. Sentiment Labeling

- Flags bullish and bearish keywords.
- Applies VADER for sentence-level polarity scoring.
- Combines multiple sentiment cues into an ensemble label (`ensemble_sentiment`).

7. Event Extraction

- Extracts named entities and noun phrases.
- Uses REBEL for structured event detection.
- Plots most frequent financial event types and their timeline.

8. Stock-Level Diagnostics

- Analyzes headline volumes per ticker and visualizes sentiment share.
- Plots ticker-specific sentiment shifts and headline bursts (e.g. for AAPL).

Outputs are used as enriched input for downstream Task 2 alignment and modeling.


**📈 How the `quantitative_analysis_orchestrator.py` Pipeline Works**

This script runs the Task 2 pipeline for the B5W1 challenge: aligning enriched sentiment signals with historical price data, computing forward returns, calculating technical indicators, and preparing a diagnostic-ready output for each stock.

📍 All outputs are saved to `data/outputs/`. The pipeline is designed to be run from the project root.

**🔁 Pipeline Steps**

1. Load Historical Price Data

- Loads all OHLCV `.csv` files from `data/yfinance_data/`, one per ticker (e.g., `AAPL_historical_data.csv`).
- Validates schema, deduplicates columns, and ensures datetime ordering.

2. Load Enriched Sentiment Data

- Uses `data/cleaned_headlines_sample.csv` from Task 1 as input.
- Parses tickers, converts dates, and aligns schema for join with price data.

3. Sentiment–Price Alignment

- Merges headline sentiment data with OHLCV time series using a ticker-date key.
- Applies exponential decay to aggregate lagged sentiment signals over a configurable window.
- Adds daily forward returns (1-day, 3-day, 5-day) for correlation diagnostics.

4. Volume–Sentiment Divergence Tagging

- Detects abnormal volume spikes using Z-score thresholds.
- Tags days where sentiment signals and volume direction disagree, suggesting hidden divergences.

5. Technical Indicator Calculation

- Computes core TA indicators per ticker using `TA-Lib`:
    - Simple Moving Average (SMA 14)
    - Exponential Moving Average (EMA 14)
    - Relative Strength Index (RSI 14)
    - MACD and Signal line
    - Average True Range (ATR 14)
- Appends results to the aligned dataframe.

6. Hybrid Performance Summary

- Computes per-ticker:
    - Annualized Return
    - Annualized Volatility
    - Sharpe Ratio (risk-free rate = 0)
    - Max Drawdown
- Summary is printed for inspection, not saved.

7. Final Output Saved

 - ✅ `enriched_full_df.csv`: Full dataset before merge
 - ✅ `enriched_aligned_df.csv`: Final sentiment–price–TA dataframe ready for modeling
- 📂 Location: `data/outputs/`

**📊 Visual Diagnostics (Optional)**
While plots were not auto-saved, the script includes logic for:

- Plotting sentiment vs price overlays
- Visualizing technical indicators over time
- Displaying divergence signals

These can be manually run via notebook for exploratory analysis or integrated into future automated runs.

### 🧠 How the `correlation_analysis_orchestrator.py` Pipeline Works

This script runs the Task 3 pipeline for the B5W1 challenge: computing statistical correlations between sentiment signals and subsequent stock price movements. It leverages exponentially weighted sentiment aggregation, multiple correlation methods, and ticker-specific diagnostics.

📍 The script is designed to be run from the project root. All visual outputs and correlation results are generated in-memory for flexible inspection and downstream reporting.

---

### 🔁 Pipeline Steps

#### 1. Load Aligned Sentiment–Price Data
- Reads the merged output from Task 2: `data/outputs/enriched_aligned_df.csv`
- Validates schema, coerces timestamp formats, and standardizes tickers.

#### 2. Daily Sentiment Aggregation
- Applies exponential decay (λ = 0.5) to compute rolling sentiment scores per ticker and date.
- Aggregated scores are stored in `agg_sentiment_ewm`.

#### 3. Correlation Feature Selection
- Dynamically selects sentiment features (e.g., `weighted_sentiment`, `agg_sentiment_ewm`) and return features (e.g., `forward_return_1d`, `return_t`, etc.).
- Ensures all required columns are available before analysis proceeds.

#### 4. Correlation Computation
- Computes per-ticker correlation matrices using:
  - Pearson (linear)
  - Spearman (rank-based)
  - Kendall (ordinal)
- Results include ticker, method, variable pairs, and correlation strength.

#### 5. Visual Diagnostics
- Plots Pearson heatmaps to show cross-variable correlation intensities.
- Displays top-N strongest Spearman correlations across tickers.
- Generates scatter plots for specific ticker–signal pairs (e.g., `AAPL`, `agg_sentiment_ewm` vs `forward_return_1d`).

---

### 📦 Outputs

- Correlation results are stored in-memory (`correlation_df`) and can be exported manually via notebook or extended pipeline logic.
- Visual plots are shown interactively and can be saved as needed (e.g., PNGs via `visualizer.save_plot()`).

---

### 🧪 Diagnostic Highlights
- Dynamic error handling ensures fallback when features or tickers are missing.
- Verbose logging prints sample data previews, correlation strength diagnostics, and failure contexts for debugging.

## 🧠 Design Philosophy
This project was developed with a focus on:

- ✅ Modular Python design using classes, helper modules, and runners (clean script folders and testable code)
- ✅ High commenting density to meet AI and human readability expectations
- ✅ Clarity (in folder structure, README, and docstrings)
- ✅ Reproducibility through consistent Git hygiene and generate_tree.py
- ✅ Rubric-alignment (clear deliverables, EDA, and insights)

## 🚀 Author
Nabil Mohamed
AIM Bootcamp Participant
GitHub: [NabloP](https://github.com/NabloP)