"""Generate synthetic Accounts Payable (AP) data.

Generates realistic AP invoices with randomized vendors, amounts, dates,
and statuses. Unposted/mismatch logic is handled downstream by the GL generator.
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
    seed: int | None = None,
    output_path: str | None = None,
) -> pl.DataFrame:
    """
    Generate synthetic Accounts Payable data with realistic variance.

    Creates vendor invoices with randomized amounts, timestamps across a 90-day
    window, and payment statuses. Reconciliation match status is not embedded here
    — it is derived by the GL generator and dbt reconciliation models.

    Args:
        n_records: Number of AP records to generate. Default 100,000.
        seed: Random seed for reproducibility. If None, non-deterministic.
        output_path: Path to save CSV. If None, no file is saved.

    Returns:
        Polars DataFrame with columns: ap_id, vendor_id, invoice_num,
        amount, invoice_date, status.

    Raises:
        ValueError: If n_records < 1.

    Example:
        >>> df = generate_accounts_payable(n_records=1_000, seed=42)
        >>> df.shape
        (1000, 6)
        >>> df["status"].value_counts().sort("status")["status"].to_list()
        ['disputed', 'paid', 'pending']
    """
    if n_records < 1:
        raise ValueError("n_records must be >= 1")

    if seed is not None:
        random.seed(seed)

    logger.info(f"Generating {n_records:,} AP records (seed={seed})")

    num_vendors = 50
    vendor_ids = generate_vendor_ids(num_vendors, prefix="VENDOR")
    invoice_numbers = generate_invoice_numbers(n_records)
    statuses = generate_status_list(n_records)

    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)

    ap_data = {
        "ap_id": [f"AP{i:08d}" for i in range(1, n_records + 1)],
        "vendor_id": [random.choice(vendor_ids) for _ in range(n_records)],
        "invoice_num": invoice_numbers,
        "amount": [generate_random_amount(100, 50_000) for _ in range(n_records)],
        "invoice_date": [generate_random_date(start_date, end_date) for _ in range(n_records)],
        "status": statuses,
    }

    df = pl.DataFrame(ap_data)

    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        df.write_csv(output_file)
        logger.info(f"Saved {n_records:,} AP records to {output_file}")

    logger.info(f"AP generation complete. Status distribution:\n{df['status'].value_counts()}")

    return df


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    output_path = (
        Path(__file__).parent.parent / "generated_data" / "raw" / "accounts_payable.csv"
    )
    generate_accounts_payable(n_records=100_000, seed=42, output_path=str(output_path))
