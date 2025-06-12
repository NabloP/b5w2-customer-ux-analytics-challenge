# Fintech UX Challenge Week 2 - 10 Academy

## 🗂 Challenge Context
This repository documents the submission for 10 Academy’s **B5W2: Customer Experience Analytics for Fintech Apps** challenge. The objective is to evaluate customer satisfaction with mobile banking apps by scraping, analyzing, and visualizing user reviews from the Google Play Store for:

- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)
- Dashen Bank

This project simulates the role of a data analyst at Omega Consultancy, advising fintechs on improving user experience and retention.

The project includes:

- 🧹 Clean scraping and preprocessing of Play Store reviews  

- 💬 Sentiment analysis (VADER, DistilBERT) and keyword clustering  

- 📊 UX pain point detection and feature insight generation  

- 🛢️ Relational database setup using Oracle XE  

- 📈 Stakeholder-ready visualizations and diagnostics

- ✅ **Streamlit App** for a seamless, non-technical user experience  


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

solar-challenge-week1/
├── LICENSE
├── README.md
├── pytest.ini
├── requirements.txt
├── .github/
│   └── workflows/
│       ├── unittests.yml
├── data/
│   ├── cleaned/
│   │   ├── reviews_CBE_20250607_124725_cleaned.csv
│   │   ├── reviews_all_banks_20250607_140803_cleaned.csv
│   │   ├── reviews_all_banks_20250607_141201_cleaned.csv
│   │   ├── reviews_all_banks_cleaned.csv
│   ├── outputs/
│   │   ├── reviews_enriched_all.csv
│   │   ├── reviews_with_sentiment_themes.csv
│   │   ├── spacy_symspell_corrected_100.csv
│   │   ├── vader_tfidf_enriched_100.csv
│   │   └── plots/
│   │       ├── average_rating_by_theme_and_bank.png
│   │       ├── boa_word_cloud.png
│   │       ├── cbe_word_cloud.png
│   │       ├── complaints_by_theme_and_bank.png
│   │       ├── dashen_word_cloud.png
│   │       ├── feature_requests_by_theme_and_bank.png
│   │       ├── user_ratings_by_bank.png
│   │       ├── y_day_rolling_sentiment_trend_per_bank.png
│   └── raw/
│       ├── reviews_BOA_20250607_124729.csv
│       ├── reviews_CBE_20250607_124725.csv
│       ├── reviews_Dashen_20250607_124733.csv
│       ├── reviews_all_banks.csv
│       ├── reviews_all_banks_20250607_140803.csv
│       ├── reviews_all_banks_20250607_141201.csv
│       ├── reviews_all_banks_20250609_121659.csv
├── models/
│   ├── mistral-7b-instruct-v0.2.Q4_K_M.gguf
│   ├── tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
│   ├── verb-form-vocab.txt
│   ├── distilbert-base-uncased-finetuned-sst-2-english/
│   │   ├── README.md
│   │   ├── config.json
│   │   ├── gitattributes (1)
│   │   ├── map.jpeg
│   │   ├── pytorch_model.bin
│   │   ├── tokenizer_config.json
│   │   ├── vocab.txt
│   └── gector_roberta_large_5k/
│       ├── README.md
│       ├── added_tokens.json
│       ├── config.json
│       ├── gitattributes
│       ├── merges.txt
│       ├── pytorch_model.bin
│       ├── special_tokens_map.json
│       ├── tokenizer.json
│       ├── tokenizer_config.json
│       ├── vocab.json
├── notebooks/
│   ├── README.md
│   ├── __init__.py
│   ├── task-1-scraping-preprocessing.ipynb
│   ├── task-2-sentiment-thematic-analysis.ipynb
│   ├── task-3-oracle-storage.ipynb
│   ├── task-4-insights-visuals.ipynb
├── scripts/
│   ├── __init__.py
│   ├── cleaning_runner.py
│   ├── generate_tree.py
│   ├── oracle_insert.py
│   ├── run_streamlit.py
│   ├── scraping_runner.py
│   ├── sentiment_pipeline.py
│   ├── visualize_insights.py
├── src/
│   ├── __init__.py
│   ├── cleaning/
│   │   ├── review_cleaner.py
│   ├── db/
│   │   ├── oracle_connector.py
│   ├── nlp/
│   │   ├── keyword_theme_extractor.py
│   │   ├── review_loader.py
│   │   ├── sentiment_classifier.py
│   │   ├── stopwords.py
│   │   ├── text_normalizer.py
│   ├── scraper/
│   │   ├── review_scraper.py
│   └── visualization/
│       ├── plot_generator.py
│       ├── theme_data_loader.py
│       ├── theme_metrics.py
├── tests/
│   ├── __init__.py
│   ├── test_data_loader.py
│   ├── test_theme_metrics.py
│   └── fixtures/
│       ├── malformed_data.csv
│       ├── malformed_themes_data.csv
│       ├── missing_column_data.csv
│       ├── theme_metrics_data.csv
│       ├── valid_data.csv
└── ui/
    ├── app_streamlit.py
<!-- TREE END -->


## ✅ Status

- ☑️ Task 1 complete: scraping and cleaning pipeline finalized

- ☑️ Task 2 complete: sentiment + theme NLP pipeline implemented and exported

- ☑️ Streamlit UI for full-cycle review management (scrape → clean)

- ☑️ Task 3 complete: Oracle XE relational storage + ER schema

- ☑️ Task 4 complete: Insight visualizations and KPI diagnostics


## 📦 What's in This Repo

This repository is structured to maximize modularity, reusability, and clarity:

- 📁 Scaffolded directory layout for pipelines, UIs, and NLP modules

- 💻 Streamlit UI for scraping and cleaning with per-bank selection, export toggles, and file previews

- 🧪 CI/CD automation via GitHub Actions for reproducibility

- 🧹 Auto-updating README structure using generate_tree.py

- 📚 Notebook-first development with clean progression through all tasks

- 🧠 NLP pipeline for sentiment scoring and thematic extraction using BERT + TF-IDF + rule-based seeds

- 📊 Diagnostic plots to support stakeholder-facing UX recommendations

- 📚 **Clear Git hygiene** (no committed `.venv` or `.csv`), commit messages and pull request usage


- 🧠 **My Contributions:** All project scaffolding, README setup, automation scripts, and CI configuration were done from scratch by me


## 🧪 Usage

### 🎛️ Option 1: Using the Streamlit App

The Streamlit UI (`ui/app_streamlit.py`) provides an interactive interface to perform both review scraping and cleaning with no code required.

**To launch the app locally:**
```bash
streamlit run ui/app_streamlit.py
```

**🧩 Streamlit Features:**

- Scrape Google Play reviews for CBE, BOA, or Dashen

- Export reviews per-bank or as a combined dataset

- Preview scraped files in-app

- Clean any raw file from `data/raw/`

- View sidebar diagnostics for:

    - Missing fields dropped

    - Blank reviews removed

    - Duplicate `reviewIds` filtered

- Download cleaned outputs directly

All exports are timestamped and saved to `data/raw/` or `data/cleaned/` depending on context.


### 🐍 Option 2: Using Python Scripts
For automated, reproducible runs from the command line or notebooks, use the modular runners in the `scripts/` folder.

**🔹 Scraping Reviews**
To scrape reviews from one or more banks and export to CSV:

```python
 scripts/scraping_runner.py --bank CBE --num_reviews 100
 ```

Options:

- `--bank`: one of `CBE`, `BOA`, `Dashen`, or `all`

- `--num_reviews`: maximum number of reviews per app


**🔹 Cleaning Reviews**
To clean a raw file and export the cleaned result:

```python 
scripts/cleaning_runner.py --input_file data/raw/reviews_BOA_20250607_124729.csv
```

This removes:

- Rows with missing fields

- Blank or whitespace-only reviews

- Duplicate entries by `reviewId`

Cleaned files are saved under `data/cleaned/`.

### 🔁 How It Works Internally

Both the Streamlit app and script-based runners share the same core logic, implemented in the following modules:

- `src/scraper/review_scraper.py` – Fetches reviews from the Play Store

- `src/cleaning/review_cleaner.py` – Cleans and validates reviews

- `src/utils/preprocessing.py` – Shared text preprocessing functions

- `scripts/run_streamlit.py` – Optional wrapper for launching UI from CLI

- `scripts/generate_tree.py` – Auto-generates folder tree for `README.md`

Each module is written using object-oriented principles and is fully reusable across CLI, notebook, and UI contexts.


### 🧠 NLP Pipeline + Storage + Visuals

This section summarizes the full enrichment, database, and insights flow from **Task 2**, **Task 3**, and **Task 4**.

---

#### 🔹 Task 2: Sentiment + Theme Enrichment

Run the full sentiment and theme extraction pipeline with:

```bash
python scripts/sentiment_pipeline.py
```

What it does:

- 🧹 Loads cleaned reviews from `data/cleaned/`

- 🔡 Normalizes text using **SymSpell** and **spaCy**

- 💬 Applies ensemble sentiment scoring:

    - `VADER`
    - `TextBlob`
    - `DistilBERT` (locally loaded from `models/`)

- 📊 Assigns each review:

    - `ensemble_sentiment` label (bullish, neutral, bearish)
    - `sentiment_uncertainty` (std deviation of ensemble)
    - `sentiment_mismatch_flag` if BERT disagrees with VADER/TextBlob

🔍 Extracts:

- Top **keywords** (via TF-IDF)

- Top **keyphrases** (noun chunking)

- UX **themes** (from curated keyword–theme dictionaries)

💾 Saves outputs to:

- `data/outputs/reviews_enriched_all.csv`

- `data/outputs/reviews_with_sentiment_themes.csv`

✅ Designed to **auto-run** with no input flags or prompts.

---

### 🛢️ Task 3: Oracle XE Database Integration (Relational Storage)

The project includes full support for enterprise-grade relational storage using Oracle XE. Reviews are inserted into a normalized schema with integrity constraints.

**Key Features:**

- ✅ `banks` and `reviews` tables in 3NF

- ✅ Modular insert logic via `oracle_insert.py`

- ✅ Connection security via `os.getenv()` (no hardcoded secrets)

- ✅ Full rollback + diagnostic prints on insert failure

- ✅ Schema DDL included for reproducibility

### 🧱 Schema Design

1. **`banks` Table**

| Column      | Type        | Description            |
|-------------|-------------|------------------------|
| `bank_id`   | INTEGER PK  | Unique bank identifier |
| `bank_name` | VARCHAR(50) | Name of the bank       |

2. reviews Table

| Column        | Type             | Description                          |
|---------------|------------------|--------------------------------------|
| `review_id`   | VARCHAR2(100) PK | Unique review ID                     |
| `bank_id`     | INTEGER FK       | Foreign key referencing banks        |
| `review_text` | CLOB             | Full text of the review              |
| `rating`      | INTEGER          | App rating (1 to 5)                  |
| `review_date` | DATE             | Parsed date of review                |
| `source`      | VARCHAR2(50)     | Always 'Google Play' in this project |

### 🔌 Usage

To insert reviews into Oracle XE after enrichment:

```bash
python scripts/oracle_insert.py
```

What it does:

- 📦 Loads enriched review file from:

    - `data/outputs/reviews_with_sentiment_themes.csv`

- 🏗️ Defines and initializes schema:

    - `reviews` table with fields for rating, sentiment, text, and metadata
    - `themes` table (if normalized)

- 🔗 Connects to Oracle XE (uses `src/db/oracle_connector.py`)

- 🧩 Inserts cleaned records with:

    - Full error handling
    - Per-row diagnostic feedback if insertions fail

- 🛑 Can be rerun idempotently (e.g. if schema already exists)

☑️ Safe to run from CLI after enrichment is complete.

📁 Related Files:

- `scripts/oracle_insert.py`: Insert runner

- `src/db/oracle_connector.py`: Secure DB connection

- `task-3-oracle-storage.ipynb`: Notebook walkthrough of schema + insert test


**📄 [Oracle XE Storage Documentation](docs/oracle_storage_overview.md)**

---

### 📈 Task 4: Visualization & KPI Dashboard
Run all Task 4 UX and sentiment visualizations with:

```bash
python scripts/visualize_insights.py
```

What it does:

- 🧠 Loads enriched reviews from `data/outputs/reviews_with_sentiment_themes.csv`

- 📊 Auto-generates plots for:

    - 📈 Average rating per theme per bank (heatmap)
    - 🔥 Complaint clusters (negative sentiment by theme and bank)
    - ☁️ Word clouds (bank-specific vocabulary)
    - 🛠️ Feature request volume (negative themes only)
    - 💎 Bubble chart for theme occurrence vs avg. rating

- 📍 Top-level theme in bubble chart is editable in-code

- 📂 Does not auto-save — plots are rendered inline

- ✅ Designed for notebook-first and CLI workflows

No flags or CLI inputs required — this script auto-runs all diagnostics sequentially.


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