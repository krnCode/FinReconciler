"""Orchestrates full data generation pipeline: AP → AR → GL.

Run this script to regenerate all three source tables in the correct order.
GL is derived from AP and AR DataFrames, so it must be generated last.

Usage:
    python scripts/generate_all.py
"""

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from generate_accounts_payable import generate_accounts_payable
from generate_accounts_receivable import generate_accounts_receivable
from generate_general_ledger import generate_general_ledger
from load_duckdb import load_raw_tables

logger = logging.getLogger(__name__)


def main(
    n_records: int = 100_000,
    seed: int = 42,
) -> None:
    """
    Generate AP, AR, and GL data tables and save them as CSVs.

    Args:
        n_records: Number of records for AP and AR tables. Default 100,000.
        seed: Random seed for reproducibility across all tables. Default 42.
    """
    raw_path = Path(__file__).parent.parent / "generated_data" / "raw"

    logger.info(f"Starting full data generation (n_records={n_records:,}, seed={seed})")

    ap_df = generate_accounts_payable(
        n_records=n_records,
        seed=seed,
        output_path=str(raw_path / "accounts_payable.csv"),
    )

    ar_df = generate_accounts_receivable(
        n_records=n_records,
        seed=seed,
        output_path=str(raw_path / "accounts_receivable.csv"),
    )

    generate_general_ledger(
        ap_df=ap_df,
        ar_df=ar_df,
        seed=seed,
        output_path=str(raw_path / "general_ledger.csv"),
    )

    load_raw_tables()

    logger.info("Data generation complete. Files saved to generated_data/raw/")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    main()
