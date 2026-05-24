"""Generate synthetic Accounts Receivable (AR) data.

This module generates realistic AR data with intentional mismatches
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


def generate_accounts_receivable(
    n_records: int = 100_000,
    mismatched_pct: float = 0.08,
    seed: int | None = None,
    output_path: str | None = None
) -> pl.DataFrame:
    """
    Generate synthetic Accounts Receivable data with realistic variance.

    Creates a dataset with customers, invoices, amounts, dates, and statuses.
    Intentionally includes mismatched records (not in GL) to test reconciliation logic.

    AR typically has higher mismatch rate than AP due to payment delays and
    partial payments.

    Args:
        n_records: Number of AR records to generate. Default 100,000.
        mismatched_pct: Percentage of records intentionally not matched in GL (0-1).
                       Default 0.08 (8% - higher than AP due to payment complexity).
        seed: Random seed for reproducibility. If None, non-deterministic.
        output_path: Path to save CSV. If None, no file is saved.

    Returns:
        Polars DataFrame with columns: ar_id, vendor_id, invoice_num,
        amount, invoice_date, status, matched_to_gl (boolean flag).

    Raises:
        ValueError: If n_records < 1 or mismatched_pct not in [0, 1].

    Example:
        >>> df = generate_accounts_receivable(n_records=10_000, seed=42)
        >>> df.shape
        (10000, 7)
        >>> df.filter(pl.col("matched_to_gl") == False).shape[0]
        800
    """
    if n_records < 1:
        raise ValueError("n_records must be >= 1")
    if not 0 <= mismatched_pct <= 1:
        raise ValueError("mismatched_pct must be between 0 and 1")

    if seed is not None:
        random.seed(seed)

    logger.info(
        f"Generating {n_records:,} AR records with {mismatched_pct*100}% "
        f"intentional mismatches (seed={seed})"
    )

    # Generate base data
    num_customers = 100  # AR typically has more customers than vendors
    customer_ids = generate_vendor_ids(num_customers, prefix="CUST")
    invoice_numbers = generate_invoice_numbers(n_records, seed=seed)

    # AR status distribution: more pending/partial due to payment delays
    ar_distribution = {'paid': 0.65, 'pending': 0.25, 'partial': 0.10}
    statuses = generate_status_list(n_records, distribution=ar_distribution, seed=seed)

    # Date range: last 90 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)

    # Generate records
    ar_data = {
        "ar_id": [f"AR{i:08d}" for i in range(1, n_records + 1)],
        "vendor_id": [random.choice(customer_ids) for _ in range(n_records)],
        "invoice_num": invoice_numbers,
        "amount": [
            generate_random_amount(500, 100000, seed=seed + i if seed else None)
            for i in range(n_records)
        ],
        "invoice_date": [
            generate_random_date(start_date, end_date, seed=seed)
            for _ in range(n_records)
        ],
        "status": statuses,
        "matched_to_gl": [
            random.random() > mismatched_pct for _ in range(n_records)
        ],
    }

    df = pl.DataFrame(ar_data)

    # Save to CSV if path provided
    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        df.write_csv(output_file)
        logger.info(f"Saved {n_records:,} AR records to {output_file}")

    logger.info(
        f"AR data generation complete. Matched: {df.filter(pl.col('matched_to_gl')).shape[0]:,}, "
        f"Unmatched: {df.filter(~pl.col('matched_to_gl')).shape[0]:,}"
    )

    return df


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Generate AR data with seed for reproducibility
    output_path = Path(__file__).parent.parent / "data" / "raw" / "accounts_receivable.csv"
    generate_accounts_receivable(
        n_records=100_000,
        mismatched_pct=0.08,
        seed=42,
        output_path=str(output_path)
    )
