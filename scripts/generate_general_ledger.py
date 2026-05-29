"""Generate synthetic General Ledger (GL) data.

This module generates realistic GL data with intentional mismatches
to simulate real-world reconciliation scenarios. GL entries are typically
aggregated from AP and AR but may have discrepancies.
"""

import logging
import random
from datetime import datetime, timedelta
from pathlib import Path

import polars as pl

from helpers import (
    generate_random_amount,
    generate_random_date,
    generate_department_names,
)

logger = logging.getLogger(__name__)


def generate_general_ledger(
    n_records: int = 100_000,
    mismatched_pct: float = 0.07,
    seed: int | None = None,
    output_path: str | None = None,
) -> pl.DataFrame:
    """
    Generate synthetic General Ledger data with realistic variance.

    Creates GL entries aggregated from AP and AR transactions. GL data has
    a different structure than AP/AR (department-based instead of
    vendor/customer-based) and intentionally includes mismatches to represent
    posting delays, reclassifications, and reconciliation issues.

    GL is the "system of truth" but may lag behind AP/AR, creating opportunities
    for reconciliation testing.

    Args:
        n_records: Number of GL records to generate. Default 100,000.
        mismatched_pct: Percentage of GL entries not fully matching AP/AR (0-1).
            Default 0.07 (7% - represents posting delays/reclassifications).
        seed: Random seed for reproducibility. If None, non-deterministic.
        output_path: Path to save CSV. If None, no file is saved.

    Returns:
        Polars DataFrame with columns: gl_id, department, amount, date,
        source_flag (AP, AR, or OTHER for mismatches).

    Raises:
        ValueError: If n_records < 1 or mismatched_pct not in [0, 1].

    Example:
        >>> df = generate_general_ledger(n_records=10_000, seed=42)
        >>> df.shape
        (10000, 5)
        >>> df.filter(pl.col("source_flag") == "OTHER").shape[0]
        700
    """
    if n_records < 1:
        raise ValueError("n_records must be >= 1")
    if not 0 <= mismatched_pct <= 1:
        raise ValueError("mismatched_pct must be between 0 and 1")

    if seed is not None:
        random.seed(seed)

    logger.info(
        f"Generating {n_records:,} GL records with {mismatched_pct*100}% "
        f"intentional mismatches (seed={seed})"
    )

    # Generate base data
    departments = generate_department_names()

    # Date range: last 90 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)

    # Generate records
    gl_data = {
        "gl_id": [f"GL{i:08d}" for i in range(1, n_records + 1)],
        "department": [random.choice(departments) for _ in range(n_records)],
        "amount": [
            generate_random_amount(200, 75000, seed=seed + i if seed else None)
            for i in range(n_records)
        ],
        "date": [
            generate_random_date(start_date, end_date, seed=seed)
            for _ in range(n_records)
        ],
        "source_flag": [
            _generate_source_flag(mismatched_pct) for _ in range(n_records)
        ],
    }

    df = pl.DataFrame(gl_data)

    # Save to CSV if path provided
    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        df.write_csv(output_file)
        logger.info(f"Saved {n_records:,} GL records to {output_file}")

    # Log summary
    source_counts = df.group_by("source_flag").agg(pl.len().alias("count"))
    logger.info(f"GL data generation complete. Source distribution:\n{source_counts}")

    return df


def _generate_source_flag(mismatched_pct: float) -> str:
    """
    Generate source flag indicating if GL entry matches AP, AR, or is OTHER.

    Args:
        mismatched_pct: Percentage of OTHER (mismatched) entries.

    Returns:
        Source flag: "AP", "AR", or "OTHER".
    """
    random_value = random.random()

    if random_value < mismatched_pct:
        return "OTHER"  # Mismatched entry (posting delay, reclassification, etc)

    # Split matched entries between AP and AR
    if random.random() < 0.5:
        return "AP"
    return "AR"


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Generate GL data with seed for reproducibility
    output_path = (
        Path(__file__).parent.parent / "generated_data" / "raw" / "general_ledger.csv"
    )
    generate_general_ledger(
        n_records=100_000, mismatched_pct=0.07, seed=42, output_path=str(output_path)
    )
