# Data Generation Documentation

**Last Updated:** 2026-05-24  
**Version:** 1.0  
**Stack:** Python 3.13+ | Polars | DuckDB

---

## Overview

This document explains how synthetic financial data is generated for the FinReconciler project. All data is created programmatically using Polars to simulate real-world Accounts Payable (AP), Accounts Receivable (AR), and General Ledger (GL) scenarios.

The generated data includes **intentional mismatches** to provide a realistic environment for testing reconciliation logic and identifying data quality issues.

---

## Data Generation Architecture

### Structure

```
scripts/
├── helpers.py                           → Reusable utility functions
├── generate_accounts_payable.py         → AP data generation
├── generate_accounts_receivable.py      → AR data generation
└── generate_general_ledger.py           → GL data generation

data/
└── raw/
    ├── accounts_payable.csv             → 100K AP records
    ├── accounts_receivable.csv          → 100K AR records
    └── general_ledger.csv               → 100K GL records
```

### Execution Flow

1. **Helper Functions** (`scripts/helpers.py`) — Provide reusable utilities for data generation
2. **AP Generation** (`generate_accounts_payable.py`) — Creates 100K vendor invoice records
3. **AR Generation** (`generate_accounts_receivable.py`) — Creates 100K customer invoice records
4. **GL Generation** (`generate_general_ledger.py`) — Creates 100K ledger entries with intentional mismatches
5. **CSV Output** — All data saved to `data/raw/` for dbt ingestion

---

## Schemas

### Accounts Payable (AP)

**Purpose:** Invoices from vendors that the company must pay.  
**Volume:** 100,000 records  
**Timespan:** 90 days of historical data

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `ap_id` | STRING | Unique AP transaction ID | `AP00000001` |
| `vendor_id` | STRING | Vendor identifier | `VENDOR00001` |
| `invoice_num` | STRING | Vendor invoice number | `INV123456` |
| `amount` | FLOAT | Invoice amount in USD | `15,234.50` |
| `invoice_date` | DATE | Date invoice was issued | `2026-03-15` |
| `status` | STRING | Payment status: paid, pending, disputed | `paid` |
| `matched_to_gl` | BOOLEAN | Whether GL posting exists | `true` |

**Key Characteristics:**
- **Vendors:** 50 unique vendors (VENDOR00001 - VENDOR00050)
- **Amount Range:** $100 - $50,000 (weighted distribution favors smaller amounts)
- **Status Distribution:** 70% paid, 20% pending, 10% disputed
- **Intentional Mismatches:** 5% of records lack GL counterpart (simulates unposted invoices)

---

### Accounts Receivable (AR)

**Purpose:** Invoices issued to customers that must be collected.  
**Volume:** 100,000 records  
**Timespan:** 90 days of historical data

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `ar_id` | STRING | Unique AR transaction ID | `AR00000001` |
| `vendor_id` | STRING | Customer identifier (vendor naming for schema consistency) | `CUST00001` |
| `invoice_num` | STRING | Sales invoice number | `INV654321` |
| `amount` | FLOAT | Invoice amount in USD | `45,678.90` |
| `invoice_date` | DATE | Date invoice was issued | `2026-03-20` |
| `status` | STRING | Collection status: paid, pending, partial | `paid` |
| `matched_to_gl` | BOOLEAN | Whether GL posting exists | `true` |

**Key Characteristics:**
- **Customers:** 100 unique customers (CUST00001 - CUST00100)
- **Amount Range:** $500 - $100,000 (weighted distribution, higher than AP)
- **Status Distribution:** 65% paid, 25% pending, 10% partial (due to partial payments)
- **Intentional Mismatches:** 8% of records lack GL counterpart (higher than AP due to collection delays)

---

### General Ledger (GL)

**Purpose:** Aggregated accounting entries consolidated from AP and AR transactions.  
**Volume:** 100,000 records  
**Timespan:** 90 days of historical data

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `gl_id` | STRING | Unique GL entry ID | `GL00000001` |
| `department` | STRING | Department that owns the entry | `Sales` |
| `amount` | FLOAT | Amount posted to GL | `32,450.75` |
| `date` | DATE | Date entry was posted | `2026-03-18` |
| `source_flag` | STRING | Origin of entry: AP, AR, or OTHER | `AP` |

**Key Characteristics:**
- **Departments:** 10 departments (Accounting, Sales, Marketing, Operations, Finance, HR, IT, Legal, Procurement, Logistics)
- **Amount Range:** $200 - $75,000 (represents consolidated/aggregated amounts)
- **Source Distribution:**
  - ~46.5% from AP source
  - ~46.5% from AR source
  - ~7% from OTHER (mismatched/reconciliation adjustments)
- **Intentional Mismatches:** 7% of records don't directly match AP or AR (simulates GL adjustments, accruals, reclassifications)

---

## Data Generation Process

### Helper Functions (`scripts/helpers.py`)

The helpers module provides reusable utilities:

| Function | Purpose |
|----------|---------|
| `generate_random_date()` | Create random dates within a range |
| `generate_random_amount()` | Create realistic financial amounts with weighted distribution |
| `generate_vendor_ids()` | Create formatted vendor/customer IDs |
| `generate_department_names()` | Return list of standard departments |
| `generate_invoice_numbers()` | Create realistic invoice numbers |
| `generate_status_list()` | Create status lists with realistic distribution |

**Design Principle:** Each function is independent and can be reused across different scripts or extended for future data generation needs.

---

### Amount Generation

Amounts use a **weighted exponential distribution** to create realistic financial data:
- Small transactions (< $1,000) are common
- Large transactions (> $40,000) are rare
- Distribution is not uniform (not all amounts equally likely)

**Formula:** `amount = min + (max - min) × (random_value ^ 0.7)`

This produces realistic variance where small invoices dominate but large ones still occur.

---

### Date Generation

Dates span **the last 90 days** from today's execution date. This ensures:
- Data is always current (relevant for reconciliation testing)
- Sufficient volume for period-over-period analysis
- Consistent timespan across all three tables

---

### Intentional Mismatches

Mismatches are purposefully created to test reconciliation logic:

| Table | Mismatch Rate | Reason |
|-------|---------------|--------|
| AP | 5% | Unposted invoices, vendor disputes |
| AR | 8% | Collection delays, partial payments, disputes |
| GL | 7% | Posting delays, accruals, reclassifications |

These are **realistic rates** based on typical financial operations.

---

## Reproducibility & Seeding

All data generation is **seeded for reproducibility**:

### Default Seed: `42`

All scripts use seed `42` by default to ensure consistent outputs:
```python
generate_accounts_payable(n_records=100_000, seed=42)
```

### Using a Different Seed

To generate different datasets, provide a different seed:
```python
generate_accounts_payable(n_records=100_000, seed=999)
```

This allows:
- Testing with different data distributions
- Validating reconciliation logic against multiple scenarios
- Creating new test datasets for different reconciliation iterations

---

## Running the Scripts

### Generate All Data at Once

```bash
cd /path/to/finreconciler

# Run AP generation
python scripts/generate_accounts_payable.py

# Run AR generation
python scripts/generate_accounts_receivable.py

# Run GL generation
python scripts/generate_general_ledger.py
```

### Generate Data Programmatically

```python
from pathlib import Path
from scripts.generate_accounts_payable import generate_accounts_payable
from scripts.generate_accounts_receivable import generate_accounts_receivable
from scripts.generate_general_ledger import generate_general_ledger

# Generate AP with custom parameters
ap_df = generate_accounts_payable(
    n_records=50_000,           # 50K records instead of 100K
    mismatched_pct=0.10,        # 10% mismatches instead of 5%
    seed=999,                   # Different seed for variation
    output_path="data/raw/ap_variant.csv"
)

# Generate AR
ar_df = generate_accounts_receivable(
    n_records=100_000,
    seed=42,
    output_path="data/raw/accounts_receivable.csv"
)

# Generate GL
gl_df = generate_general_ledger(
    n_records=100_000,
    seed=42,
    output_path="data/raw/general_ledger.csv"
)
```

---

## Output Validation

After running the generation scripts, verify the data:

### Check File Sizes

```bash
ls -lh data/raw/*.csv
# Expected: ~3-5MB per file (100K records as CSV)
```

### Validate Record Counts

```python
import polars as pl

ap = pl.read_csv("data/raw/accounts_payable.csv")
ar = pl.read_csv("data/raw/accounts_receivable.csv")
gl = pl.read_csv("data/raw/general_ledger.csv")

print(f"AP records: {ap.shape[0]}")    # Should be 100,000
print(f"AR records: {ar.shape[0]}")    # Should be 100,000
print(f"GL records: {gl.shape[0]}")    # Should be 100,000
```

### Validate Mismatches

```python
ap_matched = ap.filter(pl.col("matched_to_gl")).shape[0]
ap_unmatched = ap.filter(~pl.col("matched_to_gl")).shape[0]

print(f"AP Matched: {ap_matched} ({ap_matched/len(ap)*100:.1f}%)")
print(f"AP Unmatched: {ap_unmatched} ({ap_unmatched/len(ap)*100:.1f}%)")
# Expected: ~95% matched, ~5% unmatched
```

---

## Key Assumptions

1. **Data Independence:** AP, AR, and GL are generated independently. GL does not derive from actual AP/AR records but simulates realistic posting delays and mismatches.

2. **Deterministic Output:** With the same seed, the exact same data is always generated (bit-for-bit reproducible).

3. **Realistic Distribution:** Amounts, dates, and statuses follow realistic financial patterns (exponential amounts, uniform dates, weighted statuses).

4. **No Data Cleaning:** Raw data includes all intentional mismatches and edge cases (no filtering for "cleanliness").

5. **Single-Execution Safety:** Scripts can be run independently or together without conflicts (each creates its own CSV).

---

## Future Extensions

The modular design allows easy extensions:

### Add New Vendors
```python
# Modify helpers.generate_vendor_ids()
def generate_vendor_ids(count: int = 100):  # Increase from 50
    return [f"V{i:05d}" for i in range(1, count + 1)]
```

### Change Amount Ranges
```python
# In generate_accounts_payable.py, modify:
generate_random_amount(50, 100_000, seed=seed)  # Larger range
```

### Add More Status Values
```python
# In helpers.generate_status_list(), extend distribution:
distribution = {
    'paid': 0.65,
    'pending': 0.20,
    'disputed': 0.10,
    'cancelled': 0.05
}
```

### Generate Different Time Periods
```python
# Modify date ranges in any generation script:
end_date = datetime(2026, 6, 30)
start_date = datetime(2026, 1, 1)  # 6 months instead of 90 days
```

---

## Troubleshooting

### Import Error: `No module named 'helpers'`

**Fix:** Ensure you're running from the project root:
```bash
cd /path/to/finreconciler
python scripts/generate_accounts_payable.py  # ✅ Correct
```

Not:
```bash
cd scripts/
python generate_accounts_payable.py  # ❌ Wrong (helpers not in path)
```

### CSV File Not Created

**Check:** Verify `data/raw/` directory exists:
```bash
mkdir -p data/raw/
python scripts/generate_accounts_payable.py
```

### Memory Issues (Large Datasets)

If generating > 1M records, reduce batch size:
```python
# Generate in chunks
for batch in range(10):
    df = generate_accounts_payable(
        n_records=10_000,  # Smaller batches
        seed=42 + batch
    )
    df.write_csv(f"data/raw/accounts_payable_batch_{batch}.csv")
```

---

## References

- **Project Guide:** See `.claude/CLAUDE.md` for overall architecture
- **dbt Integration:** Raw CSV files are loaded via dbt sources (`finreconciler_dbt/models/sources.yml`)
- **Data Validation:** See dbt tests in `finreconciler_dbt/tests/` for validation logic

---

**Document Version:** 1.0  
**Last Updated:** 2026-05-24  
**Next Review:** After first dbt run with generated data
