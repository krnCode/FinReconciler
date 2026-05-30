"""Generate synthetic General Ledger (GL) data using double-entry bookkeeping.

GL entries are derived from AP and AR DataFrames. Each transaction produces two
journal lines (debit + credit) sharing the same journal_id. Controlled noise
simulates unposted invoices and manual adjustment entries.
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

CHART_OF_ACCOUNTS = {
    "1100": "Accounts Receivable",
    "2100": "Accounts Payable",
    "4000": "Revenue",
    "5000": "Operating Expense",
    "9000": "Suspense / Adjustment",
}

# Debit account, debit name, credit account, credit name
MANUAL_ACCOUNT_PAIRS = [
    ("5000", "Operating Expense", "9000", "Suspense / Adjustment"),
    ("9000", "Suspense / Adjustment", "2100", "Accounts Payable"),
    ("1100", "Accounts Receivable", "9000", "Suspense / Adjustment"),
]


def generate_general_ledger(
    ap_df: pl.DataFrame,
    ar_df: pl.DataFrame,
    ap_unposted_pct: float = 0.05,
    ar_unposted_pct: float = 0.08,
    manual_entry_count: int = 3_000,
    seed: int | None = None,
    output_path: str | None = None,
) -> pl.DataFrame:
    """
    Generate General Ledger entries derived from AP and AR data.

    Implements double-entry bookkeeping: every transaction produces one debit line
    and one credit line sharing the same journal_id. The document_ref column links
    GL entries back to their source AP/AR invoice number, enabling reconciliation.

    Controlled noise:
      - ap_unposted_pct: AP invoices intentionally absent from GL (unposted).
      - ar_unposted_pct: AR invoices intentionally absent from GL.
      - manual_entry_count: Orphan GL entries with no AP/AR source (adjustments,
        accruals, reclassifications).

    Args:
        ap_df: Accounts Payable DataFrame from generate_accounts_payable().
        ar_df: Accounts Receivable DataFrame from generate_accounts_receivable().
        ap_unposted_pct: Fraction of AP invoices with no GL posting. Default 0.05.
        ar_unposted_pct: Fraction of AR invoices with no GL posting. Default 0.08.
        manual_entry_count: Number of manual journal entries to generate. Default 3,000.
        seed: Random seed for reproducibility. If None, non-deterministic.
        output_path: Path to save CSV. If None, no file is saved.

    Returns:
        Polars DataFrame with columns: gl_id, journal_id, document_ref,
        account_code, account_name, department, amount, entry_type,
        entry_description, source_system, posting_date, status.

    Raises:
        ValueError: If unposted percentages not in [0, 1] or manual_entry_count < 0.

    Example:
        >>> import random
        >>> random.seed(42)
        >>> ap = generate_accounts_payable(n_records=1_000, seed=42)
        >>> ar = generate_accounts_receivable(n_records=1_000, seed=42)
        >>> gl = generate_general_ledger(ap, ar, seed=42)
        >>> gl.columns
        ['gl_id', 'journal_id', 'document_ref', 'account_code', 'account_name',
         'department', 'amount', 'entry_type', 'entry_description',
         'source_system', 'posting_date', 'status']
    """
    if not 0 <= ap_unposted_pct <= 1:
        raise ValueError("ap_unposted_pct must be between 0 and 1")
    if not 0 <= ar_unposted_pct <= 1:
        raise ValueError("ar_unposted_pct must be between 0 and 1")
    if manual_entry_count < 0:
        raise ValueError("manual_entry_count must be non-negative")

    if seed is not None:
        random.seed(seed)

    departments = generate_department_names()
    all_segments: list[pl.DataFrame] = []
    journal_counter = 1

    # --- AP journals ---
    n_ap_to_post = int(len(ap_df) * (1 - ap_unposted_pct))
    ap_posted = ap_df.sample(n=n_ap_to_post, seed=seed, shuffle=True)

    ap_journal_ids = [f"JNL{journal_counter + i:08d}" for i in range(n_ap_to_post)]
    journal_counter += n_ap_to_post

    ap_inv_dates = ap_posted["invoice_date"].to_list()
    ap_posting_dates = [d + timedelta(days=random.randint(0, 3)) for d in ap_inv_dates]
    ap_departments = [random.choice(departments) for _ in range(n_ap_to_post)]
    ap_descriptions = [
        f"AP Invoice {inv_num} | Vendor {vendor_id} | {_fmt_date(inv_date)}"
        for inv_num, vendor_id, inv_date in zip(
            ap_posted["invoice_num"].to_list(),
            ap_posted["vendor_id"].to_list(),
            ap_inv_dates,
        )
    ]

    ap_base = ap_posted.select([
        pl.col("invoice_num").alias("document_ref"),
        pl.col("amount"),
    ]).with_columns([
        pl.Series("journal_id", ap_journal_ids),
        pl.Series("department", ap_departments),
        pl.Series("posting_date", ap_posting_dates),
        pl.Series("entry_description", ap_descriptions),
        pl.lit("AP").alias("source_system"),
        pl.lit("posted").alias("status"),
    ])

    all_segments.append(
        ap_base.with_columns([
            pl.lit("5000").alias("account_code"),
            pl.lit("Operating Expense").alias("account_name"),
            pl.lit("debit").alias("entry_type"),
        ])
    )
    all_segments.append(
        ap_base.with_columns([
            pl.lit("2100").alias("account_code"),
            pl.lit("Accounts Payable").alias("account_name"),
            pl.lit("credit").alias("entry_type"),
        ])
    )

    logger.info(
        f"AP: {n_ap_to_post:,} posted, {len(ap_df) - n_ap_to_post:,} unposted"
    )

    # --- AR journals ---
    n_ar_to_post = int(len(ar_df) * (1 - ar_unposted_pct))
    ar_posted = ar_df.sample(n=n_ar_to_post, seed=seed, shuffle=True)

    ar_journal_ids = [f"JNL{journal_counter + i:08d}" for i in range(n_ar_to_post)]
    journal_counter += n_ar_to_post

    ar_inv_dates = ar_posted["invoice_date"].to_list()
    ar_posting_dates = [d + timedelta(days=random.randint(0, 3)) for d in ar_inv_dates]
    ar_departments = [random.choice(departments) for _ in range(n_ar_to_post)]
    ar_descriptions = [
        f"AR Invoice {inv_num} | Customer {customer_id} | {_fmt_date(inv_date)}"
        for inv_num, customer_id, inv_date in zip(
            ar_posted["invoice_num"].to_list(),
            ar_posted["vendor_id"].to_list(),
            ar_inv_dates,
        )
    ]

    ar_base = ar_posted.select([
        pl.col("invoice_num").alias("document_ref"),
        pl.col("amount"),
    ]).with_columns([
        pl.Series("journal_id", ar_journal_ids),
        pl.Series("department", ar_departments),
        pl.Series("posting_date", ar_posting_dates),
        pl.Series("entry_description", ar_descriptions),
        pl.lit("AR").alias("source_system"),
        pl.lit("posted").alias("status"),
    ])

    all_segments.append(
        ar_base.with_columns([
            pl.lit("1100").alias("account_code"),
            pl.lit("Accounts Receivable").alias("account_name"),
            pl.lit("debit").alias("entry_type"),
        ])
    )
    all_segments.append(
        ar_base.with_columns([
            pl.lit("4000").alias("account_code"),
            pl.lit("Revenue").alias("account_name"),
            pl.lit("credit").alias("entry_type"),
        ])
    )

    logger.info(
        f"AR: {n_ar_to_post:,} posted, {len(ar_df) - n_ar_to_post:,} unposted"
    )

    # --- Manual / adjustment journals ---
    if manual_entry_count > 0:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)

        manual_journal_ids = [
            f"JNL{journal_counter + i:08d}" for i in range(manual_entry_count)
        ]

        manual_amounts = [generate_random_amount(500, 50_000) for _ in range(manual_entry_count)]
        manual_depts = [random.choice(departments) for _ in range(manual_entry_count)]
        manual_entry_dates = [generate_random_date(start_date, end_date) for _ in range(manual_entry_count)]
        manual_posting_dates = [d + timedelta(days=random.randint(0, 5)) for d in manual_entry_dates]
        manual_statuses = ["pending" if random.random() < 0.10 else "posted" for _ in range(manual_entry_count)]
        manual_pairs = [random.choice(MANUAL_ACCOUNT_PAIRS) for _ in range(manual_entry_count)]
        manual_descriptions = [
            f"Manual Entry {jnl_id} | Dept: {dept} | Period: {d.strftime('%Y-%m')}"
            for jnl_id, dept, d in zip(manual_journal_ids, manual_depts, manual_entry_dates)
        ]

        manual_debit_df = pl.DataFrame({
            "document_ref": pl.Series([None] * manual_entry_count, dtype=pl.Utf8),
            "amount": manual_amounts,
            "journal_id": manual_journal_ids,
            "department": manual_depts,
            "posting_date": manual_posting_dates,
            "entry_description": manual_descriptions,
            "source_system": ["MANUAL"] * manual_entry_count,
            "status": manual_statuses,
            "account_code": [p[0] for p in manual_pairs],
            "account_name": [p[1] for p in manual_pairs],
            "entry_type": ["debit"] * manual_entry_count,
        })

        manual_credit_df = pl.DataFrame({
            "document_ref": pl.Series([None] * manual_entry_count, dtype=pl.Utf8),
            "amount": manual_amounts,
            "journal_id": manual_journal_ids,
            "department": manual_depts,
            "posting_date": manual_posting_dates,
            "entry_description": manual_descriptions,
            "source_system": ["MANUAL"] * manual_entry_count,
            "status": manual_statuses,
            "account_code": [p[2] for p in manual_pairs],
            "account_name": [p[3] for p in manual_pairs],
            "entry_type": ["credit"] * manual_entry_count,
        })

        all_segments.extend([manual_debit_df, manual_credit_df])
        logger.info(f"Manual: {manual_entry_count:,} entries generated")

    # Combine, sort by journal_id so each pair of lines is adjacent, assign gl_id
    df = pl.concat(all_segments, how="diagonal").sort("journal_id")
    n_rows = len(df)
    df = df.with_columns(
        pl.Series("gl_id", [f"GL{i:08d}" for i in range(1, n_rows + 1)])
    )

    df = df.select([
        "gl_id", "journal_id", "document_ref", "account_code", "account_name",
        "department", "amount", "entry_type", "entry_description",
        "source_system", "posting_date", "status",
    ])

    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        df.write_csv(output_file)
        logger.info(f"Saved {n_rows:,} GL entries to {output_file}")

    total_journals = n_ap_to_post + n_ar_to_post + manual_entry_count
    logger.info(
        f"GL generation complete: {total_journals:,} journals, {n_rows:,} total lines"
    )

    return df


def _fmt_date(dt: object) -> str:
    """Format a datetime-like object as YYYY-MM-DD string."""
    if hasattr(dt, "strftime"):
        return dt.strftime("%Y-%m-%d")
    return str(dt)[:10]


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    raw_path = Path(__file__).parent.parent / "generated_data" / "raw"
    ap_path = raw_path / "accounts_payable.csv"
    ar_path = raw_path / "accounts_receivable.csv"

    if not ap_path.exists() or not ar_path.exists():
        logger.error(
            "AP/AR CSVs not found. Run generate_accounts_payable.py and "
            "generate_accounts_receivable.py first, or use generate_all.py."
        )
        raise SystemExit(1)

    ap_df = pl.read_csv(ap_path, try_parse_dates=True)
    ar_df = pl.read_csv(ar_path, try_parse_dates=True)

    generate_general_ledger(
        ap_df=ap_df,
        ar_df=ar_df,
        seed=42,
        output_path=str(raw_path / "general_ledger.csv"),
    )
