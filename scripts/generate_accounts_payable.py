"""Generate synthetic Accounts Payable (AP) data.

This module generates realistic AP data with intentional mismatches
to simulate real-world reconciliation scenarios.
"""

import logging
import random
from datetime import datetime, timedelta
from pathlib import Path

import polars as pl

from helpers import (
    generate_random_amount,
    generate_random_date,
    generate_vendor_ids,
    generate_invoice_numbers,
    generate_status_list,
)

logger = logging.getLogger(__name__)


def generate_accounts_payable(
    n_records: int = 100_000,
    mismatched_pct: float = 0.05,
    seed: int | None = None,
    output_path: str | None = None,
) -> pl.DataFrame:
    """
    Generate synthetic Accounts Payable data with realistic variance.

    Creates a dataset with vendors, invoices, amounts, dates, and statuses.
    Intentionally includes mismatched records (not in GL) to test reconciliation logic.

    Args:
        n_records: Number of AP records to generate. Default 100,000.
        mismatched_pct: Percentage of records intentionally not matched in GL (0-1).
            Default 0.05 (5%).
        seed: Random seed for reproducibility. If None, non-deterministic.
        output_path: Path to save CSV. If None, no file is saved.

    Returns:
        Polars DataFrame with columns: ap_id, vendor_id, invoice_num,
        amount, invoice_date, status, matched_to_gl (boolean flag).

    Raises:
        ValueError: If n_records < 1 or mismatched_pct not in [0, 1].

    Example:
        >>> df = generate_accounts_payable(n_records=10_000, seed=42)
        >>> df.shape
        (10000, 7)
        >>> df.filter(pl.col("matched_to_gl") == False).shape[0]
        500
    """
    if n_records < 1:
        raise ValueError("n_records must be >= 1")
    if not 0 <= mismatched_pct <= 1:
        raise ValueError("mismatched_pct must be between 0 and 1")

    if seed is not None:
        random.seed(seed)

    logger.info(
        f"Generating {n_records:,} AP records with {mismatched_pct*100}% "
        f"intentional mismatches (seed={seed})"
    )

    # Generate base data
    num_vendors = 50
    vendor_ids = generate_vendor_ids(num_vendors, prefix="VENDOR")
    invoice_numbers = generate_invoice_numbers(n_records, seed=seed)
    statuses = generate_status_list(n_records, seed=seed)

    # Date range: last 90 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)

    # Generate records
    ap_data = {
        "ap_id": [f"AP{i:08d}" for i in range(1, n_records + 1)],
        "vendor_id": [random.choice(vendor_ids) for _ in range(n_records)],
        "invoice_num": invoice_numbers,
        "amount": [
            generate_random_amount(100, 50000, seed=seed + i if seed else None)
            for i in range(n_records)
        ],
        "invoice_date": [
            generate_random_date(start_date, end_date, seed=seed)
            for _ in range(n_records)
        ],
        "status": statuses,
        "matched_to_gl": [random.random() > mismatched_pct for _ in range(n_records)],
    }

    df = pl.DataFrame(ap_data)

    # Save to CSV if path provided
    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        df.write_csv(output_file)
        logger.info(f"Saved {n_records:,} AP records to {output_file}")

    logger.info(
        f"AP data generation complete. Matched: {df.filter(pl.col('matched_to_gl')).shape[0]:,}, "
        f"Unmatched: {df.filter(~pl.col('matched_to_gl')).shape[0]:,}"
    )

    return df


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Generate AP data with seed for reproducibility
    output_path = (
        Path(__file__).parent.parent / "generated_data" / "raw" / "accounts_payable.csv"
    )
    generate_accounts_payable(
        n_records=100_000, mismatched_pct=0.05, seed=42, output_path=str(output_path)
    )
