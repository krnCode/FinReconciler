"""Load raw CSVs from generated_data/raw into DuckDB.

Run this after generate_all.py and before dbt run.

Usage:
    python scripts/load_duckdb.py
"""

import logging
import duckdb

from pathlib import Path

logger = logging.getLogger(__name__)

DB_PATH = (
    Path(__file__).parent.parent / "generated_data" / "duckdb" / "finreconciler.duckdb"
)
RAW_PATH = Path(__file__).parent.parent / "generated_data" / "raw"

TABLES = {
    "accounts_payable": RAW_PATH / "accounts_payable.csv",
    "accounts_receivable": RAW_PATH / "accounts_receivable.csv",
    "general_ledger": RAW_PATH / "general_ledger.csv",
}


def load_raw_tables() -> None:
    """Load all raw CSVs into DuckDB main schema, replacing existing tables."""
    conn = duckdb.connect(str(DB_PATH))

    for table_name, csv_path in TABLES.items():
        if not csv_path.exists():
            raise FileNotFoundError(
                f"CSV not found: {csv_path}. Run generate_all.py first."
            )

        logger.info(f"Loading {table_name} from {csv_path.name}...")
        conn.execute(f"""
            create or replace table main.{table_name} as
            select * from read_csv_auto('{csv_path.as_posix()}', header = true)
        """)
        count = conn.execute(f"select count(*) from main.{table_name}").fetchone()[0]
        logger.info(f"  → {count:,} rows loaded into main.{table_name}")

    conn.close()
    logger.info("All tables loaded successfully.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    load_raw_tables()
