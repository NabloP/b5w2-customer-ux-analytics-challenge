"""
oracle_insert.py – Ingestion Script for Enriched Reviews (B5W2)
-----------------------------------------------------------------

Runs the Task 3 database ingestion pipeline: drops/creates schema and bulk-loads
cleaned & enriched Google Play reviews into Oracle using the OracleConnector module.

Features:
- Idempotent schema deployment (skips existing tables)
- Bulk insertion of banks and reviews with foreign key mapping
- Robust error handling and debug logging

Author: Nabil Mohamed
"""

# ------------------------------------------------------------------------------
# 🛠 Ensure Script Runs from Project Root (for src/ imports to work)
# ------------------------------------------------------------------------------
import os  # stdlib: OS utilities
import sys  # stdlib: system path manipulation

# If executed from a subfolder (e.g., /notebooks), move up to project root
if os.path.basename(os.getcwd()) in ("notebooks", "scripts"):
    os.chdir("..")
    print("📂 Changed working directory to project root")

# Capture and add project root to sys.path for module imports
project_root = os.getcwd()
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"✅ Added to sys.path: {project_root}")

# Optional verification of data folder presence
expected_data = "data/outputs/reviews_enriched_all.csv"
print(
    "📁 Enriched data path ready"
    if os.path.exists(expected_data)
    else f"⚠️ Enriched data not found: {expected_data}"
)

# ------------------------------------------------------------------------------
# 🚀 Task 3 – Deploy Schema & Load Enriched Reviews
# ------------------------------------------------------------------------------
from src.db.oracle_connector import OracleConnector  # our OOP ingestion module

# Path to the enriched reviews CSV (relative to project root)
CSV_RELATIVE = "data/outputs/reviews_enriched_all.csv"

try:
    # Initialize connector with debug logging enabled
    connector = OracleConnector(verbose=True)

    # Idempotently drop existing tables
    connector.drop_tables()

    # Idempotently create banks & reviews tables
    connector.create_schema()

    # Bulk-load enriched reviews into Oracle
    connector.load_data(csv_relative=CSV_RELATIVE)

    # Close the database connection
    connector.close()

    # Success message
    print("🎉 Task 3 complete: schema deployed and data loaded successfully.")

# Top-level error handling: ensure cleanup and report failure
except Exception as e:
    print(f"❌ Task 3 failed: {e}")
    try:
        connector.close()
    except:
        pass
