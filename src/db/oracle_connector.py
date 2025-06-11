"""
oracle_connector.py – Oracle Database Ingestion Module (B5W2)
--------------------------------------------------------------

Provides an Object-Oriented interface for Task 3: persisting cleaned and enriched
Google Play reviews into an Oracle database. Handles schema deployment, data loading,
and connection management with robust error handling, debug logging, and idempotence.

Author: Nabil Mohamed
"""

import os  # stdlib: environment
import csv  # stdlib: CSV parsing
from pathlib import Path  # stdlib: filesystem paths
from datetime import datetime  # stdlib: date parsing
from dotenv import load_dotenv  # 3rd-party: load .env files
import oracledb  # 3rd-party: Oracle DB driver
import logging  # stdlib: logging

# -------------------------------------------------------------------------------
# 🗄️ OracleConnector – Manages Oracle DB connection, schema, and data loading
# -------------------------------------------------------------------------------


class OracleConnector:
    """
    Encapsulates Oracle DB operations for Task 3.

    Attributes:
    -----------
    env_path : Path
        Path to the .env file containing ORACLE_USER, ORACLE_PASS, ORACLE_DSN.
    user : str
        Oracle username loaded from environment.
    password : str
        Oracle password loaded from environment.
    dsn : str
        Oracle DSN (host:port/service_name) loaded from environment.
    conn : oracledb.Connection | None
        Cached Oracle connection instance.
    logger : logging.Logger
        Logger for debug/info messages.
    """

    def __init__(self, env_file: Path = None, verbose: bool = True):
        # Determine project root (src/db → project root)
        project_root = Path(__file__).resolve().parent.parent

        # Load .env from specified path or project root/.env
        self.env_path = env_file or (project_root / ".env")
        load_dotenv(self.env_path, override=True)

        # Read and validate credentials
        self.user = os.getenv("ORACLE_USER")
        self.password = os.getenv("ORACLE_PASS")
        self.dsn = os.getenv("ORACLE_DSN")
        missing = [
            k
            for k, v in {
                "ORACLE_USER": self.user,
                "ORACLE_PASS": self.password,
                "ORACLE_DSN": self.dsn,
            }.items()
            if not v
        ]
        if missing:
            raise RuntimeError(f"Missing env vars: {', '.join(missing)}")

        # Configure logging
        level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(message)s")
        self.logger = logging.getLogger("OracleConnector")
        self.logger.debug(f"Env loaded → user={self.user}, dsn={self.dsn}")

        # Placeholder for DB connection
        self.conn = None

    def connect(self) -> oracledb.Connection:
        """Lazily establish and cache the Oracle DB connection."""
        if self.conn is None:
            self.conn = oracledb.connect(
                user=self.user, password=self.password, dsn=self.dsn
            )
            self.logger.info(f"✅ Connected as {self.conn.username}")
        return self.conn

    def close(self) -> None:
        """Close the connection if open."""
        if self.conn:
            self.conn.close()
            self.logger.info("🔒 Connection closed")
            self.conn = None

    def _table_exists(self, table: str) -> bool:
        """
        Check existence of a table in the user schema.

        Parameters:
        -----------
        table : str
            Name of the table to check.

        Returns:
        --------
        bool : True if the table exists, False otherwise.
        """
        cur = self.connect().cursor()
        cur.execute(
            "SELECT COUNT(*) FROM user_tables WHERE table_name = :t",
            {"t": table.upper()},
        )
        exists = cur.fetchone()[0] > 0
        cur.close()
        self.logger.debug(f"Table '{table}' exists? {exists}")
        return exists

    def drop_tables(self) -> None:
        """
        Idempotently drop 'reviews' and 'banks' tables if they exist.
        """
        for table in ("reviews", "banks"):
            if self._table_exists(table):
                try:
                    self.connect().cursor().execute(
                        f"DROP TABLE {table} CASCADE CONSTRAINTS"
                    )
                    self.logger.info(f"➖ Dropped existing table '{table}'")
                except Exception as e:
                    self.logger.error(f"Failed to drop '{table}': {e}")
                finally:
                    self.conn.commit()
            else:
                self.logger.info(f"➖ Table '{table}' not found; skipping drop")

    def create_schema(self) -> None:
        """
        Idempotently create 'banks' and 'reviews' tables (with FK).
        """
        cur = self.connect().cursor()

        # Create 'banks' if missing
        if not self._table_exists("banks"):
            cur.execute(
                """
CREATE TABLE banks (
  bank_id   NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  bank_name VARCHAR2(100) UNIQUE
)"""
            )
            self.logger.info("✅ Created table 'banks'")
        else:
            self.logger.info("ℹ️ Table 'banks' already exists; skipping creation")

        # Create 'reviews' if missing
        if not self._table_exists("reviews"):
            cur.execute(
                """
CREATE TABLE reviews (
  review_pk         NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  review_id         VARCHAR2(100) UNIQUE,
  review_text       CLOB,
  rating            NUMBER(1),
  review_date       DATE,
  bank_id           NUMBER REFERENCES banks(bank_id),
  source            VARCHAR2(50),
  normalized_review CLOB,
  bert_score        NUMBER,
  vader_score       NUMBER,
  textblob_score    NUMBER,
  ensemble_score    NUMBER,
  label             VARCHAR2(50),
  uncertainty       NUMBER,
  rule_label        VARCHAR2(50),
  flag              CHAR(1)
)"""
            )
            self.logger.info("✅ Created table 'reviews'")
        else:
            self.logger.info("ℹ️ Table 'reviews' already exists; skipping creation")

        cur.close()
        self.conn.commit()

    def load_data(
        self, csv_relative: str = "data/outputs/reviews_enriched_all.csv"
    ) -> None:
        """
        Bulk-load distinct banks and review rows from a CSV file.

        Parameters:
        -----------
        csv_relative : str
            Relative path (from project root) to the enriched CSV file.
        """
        # Resolve CSV path
        project_root = (
            Path(__file__).resolve().parents[2]
        )  # up three levels to <project>
        csv_path = (
            project_root / csv_relative
        )  # now points to <project>/data/outputs/reviews_enriched_all.csv

        # Parse CSV into memory
        bank_set, records = set(), []
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                bank_set.add(row["bank"])
                records.append(
                    {
                        "review_id": row["reviewId"],
                        "review_text": row["review"],
                        "rating": float(row["rating"]),
                        "review_date": datetime.strptime(row["date"], "%Y-%m-%d"),
                        "bank": row["bank"],
                        "source": row["source"],
                        "normalized_review": row["normalized_review"],
                        "bert_score": float(row["bert"]),
                        "vader_score": float(row["vader"]),
                        "textblob_score": float(row["textblob"]),
                        "ensemble_score": float(row["ensemble"]),
                        "label": row["label"],
                        "uncertainty": float(row["uncertainty"]),
                        "rule_label": row["rule_label"],
                        "flag": "1" if row["flag"].lower() in ("1", "true") else "0",
                    }
                )
        self.logger.debug(f"Parsed {len(records)} rows, {len(bank_set)} banks")

        # Insert banks
        bank_rows = [(b,) for b in sorted(bank_set)]
        cur = self.connect().cursor()
        cur.executemany("INSERT INTO banks (bank_name) VALUES (:1)", bank_rows)
        cur.close()
        self.conn.commit()
        self.logger.info(f"Inserted {len(bank_rows)} banks")

        # Build mapping
        cur = self.connect().cursor()
        cur.execute("SELECT bank_id, bank_name FROM banks")
        bank_map = {name: bid for bid, name in cur.fetchall()}
        cur.close()

        # Prepare and insert reviews
        insert_sql = """
INSERT INTO reviews (
  review_id, review_text, rating, review_date, bank_id, source,
  normalized_review, bert_score, vader_score,
  textblob_score, ensemble_score, label,
  uncertainty, rule_label, flag
) VALUES (
  :1, :2, :3, :4, :5, :6,
  :7, :8, :9,
  :10, :11, :12,
  :13, :14, :15
)"""
        batch = []
        for rec in records:
            batch.append(
                (
                    rec["review_id"],
                    rec["review_text"],
                    rec["rating"],
                    rec["review_date"],
                    bank_map[rec["bank"]],
                    rec["source"],
                    rec["normalized_review"],
                    rec["bert_score"],
                    rec["vader_score"],
                    rec["textblob_score"],
                    rec["ensemble_score"],
                    rec["label"],
                    rec["uncertainty"],
                    rec["rule_label"],
                    rec["flag"],
                )
            )
        cur = self.connect().cursor()
        cur.executemany(insert_sql, batch)
        cur.close()
        self.conn.commit()
        self.logger.info(f"Loaded {len(batch)} reviews")


# Script entrypoint
if __name__ == "__main__":
    oc = OracleConnector()
    oc.drop_tables()
    oc.create_schema()
    oc.load_data()
    oc.close()
