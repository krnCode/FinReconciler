"""Generate synthetic Accounts Receivable (AR) data.

Generates realistic AR invoices with randomized customers, amounts, dates,
and collection statuses. Unposted/mismatch logic is handled downstream by the GL generator.
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
    seed: int | None = None,
    output_path: str | None = None,
) -> pl.DataFrame:
    """
    Generate synthetic Accounts Receivable data with realistic variance.

    Creates customer invoices with randomized amounts, timestamps across a 90-day
    window, and collection statuses. AR typically carries higher mismatch rates than AP
    due to partial payments and collection delays — this is handled by the GL generator.

    Args:
        n_records: Number of AR records to generate. Default 100,000.
        seed: Random seed for reproducibility. If None, non-deterministic.
        output_path: Path to save CSV. If None, no file is saved.

    Returns:
        Polars DataFrame with columns: ar_id, vendor_id, invoice_num,
        amount, invoice_date, status.

    Raises:
        ValueError: If n_records < 1.

    Example:
        >>> df = generate_accounts_receivable(n_records=1_000, seed=42)
        >>> df.shape
        (1000, 6)
        >>> df["status"].value_counts().sort("status")["status"].to_list()
        ['paid', 'partial', 'pending']
    """
    if n_records < 1:
        raise ValueError("n_records must be >= 1")

    if seed is not None:
        random.seed(seed)

    logger.info(f"Generating {n_records:,} AR records (seed={seed})")

    num_customers = 100
    customer_ids = generate_vendor_ids(num_customers, prefix="CUST")
    invoice_numbers = generate_invoice_numbers(n_records)

    ar_distribution = {"paid": 0.65, "pending": 0.25, "partial": 0.10}
    statuses = generate_status_list(n_records, distribution=ar_distribution)

    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)

    ar_data = {
        "ar_id": [f"AR{i:08d}" for i in range(1, n_records + 1)],
        "vendor_id": [random.choice(customer_ids) for _ in range(n_records)],
        "invoice_num": invoice_numbers,
        "amount": [generate_random_amount(500, 100_000) for _ in range(n_records)],
        "invoice_date": [generate_random_date(start_date, end_date) for _ in range(n_records)],
        "status": statuses,
    }

    df = pl.DataFrame(ar_data)

    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        df.write_csv(output_file)
        logger.info(f"Saved {n_records:,} AR records to {output_file}")

    logger.info(f"AR generation complete. Status distribution:\n{df['status'].value_counts()}")

    return df


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    output_path = (
        Path(__file__).parent.parent / "generated_data" / "raw" / "accounts_receivable.csv"
    )
    generate_accounts_receivable(n_records=100_000, seed=42, output_path=str(output_path))
