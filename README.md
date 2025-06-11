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
├── requirements.txt
├── .github/
│   └── workflows/
│       ├── unittests.yml
├── data/
│   ├── cleaned/
│   │   ├── reviews_all_banks_20250607_140803_cleaned.csv
│   │   ├── reviews_all_banks_20250607_141201_cleaned.csv
│   │   ├── reviews_all_banks_cleaned.csv
│   ├── outputs/
│   └── raw/
│       ├── reviews_BOA_20250607_124729.csv
│       ├── reviews_CBE_20250607_124725.csv
│       ├── reviews_Dashen_20250607_124733.csv
│       ├── reviews_all_banks.csv
│       ├── reviews_all_banks_20250607_140803.csv
│       ├── reviews_all_banks_20250607_141201.csv
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
│   │   ├── sentiment_classifier.py
│   ├── scraper/
│   │   ├── review_scraper.py
│   └── utils/
│       ├── preprocessing.py
├── tests/
│   ├── __init__.py
└── ui/
    ├── app_streamlit.py
<!-- TREE END -->


## ✅ Status

- ☑️ Task 1 complete: scraping and cleaning pipeline finalized

- ☑️ Streamlit UI for end-to-end data collection and preprocessing

- ☑️ Modular architecture for reuse in scripts and notebooks

- ☑️ Row diagnostics and metadata tracking implemented

- ☑️ Ready for Task 2: Sentiment & Thematic NLP Pipeline


## 📦 What's in This Repo

This repository is structured to maximize modularity, reusability, and clarity:

- 📁 Scaffolded directory layout for pipelines, UIs, and NLP modules
- 💻 Streamlit UI for scraping and cleaning with per-bank selection, export toggles, and file previews
- 🧪 CI/CD automation via GitHub Actions for reproducibility
- 🧹 Auto-updating README structure using generate_tree.py
- 📚 Notebook-first development with clean progression through all tasks
This repository documents the Week 1 challenge for 10 Academy’s AI Mastery Bootcamp. It includes:

- 📁 **Scaffolded directory structure** using best practices for `src/`, `notebooks/`, `scripts/`, and `tests/`

- 💻 Streamlit UI for scraping and cleaning with per-bank selection, export toggles, and file previews

- 🧪 **CI/CD integration** via GitHub Actions for reproducibility and reliability

- 🧹 **README auto-updating** via `scripts/generate_tree.py` to keep documentation aligned with project layout

- 📚 Notebook-first development with clean progression through all tasks

- 📊 Modular EDA workflows for review cleaning, UX issue detection, and app-specific user sentiment

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