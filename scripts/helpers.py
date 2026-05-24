"""Helper functions for synthetic financial data generation.

This module provides reusable utilities for generating realistic financial data,
including random dates, amounts, and other financial attributes.
"""

import random
from datetime import datetime, timedelta
from typing import List


def generate_random_date(
    start_date: datetime,
    end_date: datetime,
    seed: int | None = None
) -> datetime:
    """
    Generate a random date between start_date and end_date.

    Args:
        start_date: The earliest possible date.
        end_date: The latest possible date.
        seed: Random seed for reproducibility. If None, non-deterministic.

    Returns:
        A random datetime object between start_date and end_date.

    Raises:
        ValueError: If start_date is after end_date.

    Example:
        >>> start = datetime(2026, 1, 1)
        >>> end = datetime(2026, 3, 31)
        >>> date = generate_random_date(start, end, seed=42)
        >>> start <= date <= end
        True
    """
    if start_date > end_date:
        raise ValueError("start_date must be before or equal to end_date")

    if seed is not None:
        random.seed(seed)

    time_delta = end_date - start_date
    random_seconds = random.randint(0, int(time_delta.total_seconds()))
    return start_date + timedelta(seconds=random_seconds)


def generate_random_amount(
    min_amount: float,
    max_amount: float,
    seed: int | None = None,
    decimal_places: int = 2
) -> float:
    """
    Generate a random amount between min_amount and max_amount.

    Uses weighted distribution to create realistic financial amounts
    (more small transactions, fewer large ones).

    Args:
        min_amount: Minimum amount value.
        max_amount: Maximum amount value.
        seed: Random seed for reproducibility. If None, non-deterministic.
        decimal_places: Number of decimal places to round to.

    Returns:
        A random float amount with specified decimal places.

    Raises:
        ValueError: If min_amount is negative or greater than max_amount.

    Example:
        >>> amount = generate_random_amount(100, 50000, seed=42)
        >>> 100 <= amount <= 50000
        True
    """
    if min_amount < 0:
        raise ValueError("min_amount must be non-negative")
    if min_amount > max_amount:
        raise ValueError("min_amount must be less than or equal to max_amount")

    if seed is not None:
        random.seed(seed)

    # Use weighted distribution (exponential-like) for realistic amounts
    random_value = random.random()
    amount = min_amount + (max_amount - min_amount) * (random_value ** 0.7)
    return round(amount, decimal_places)


def generate_vendor_ids(
    count: int,
    prefix: str = "V"
) -> List[str]:
    """
    Generate a list of vendor IDs.

    Args:
        count: Number of vendor IDs to generate.
        prefix: Prefix for vendor IDs (default: "V").

    Returns:
        A list of vendor IDs formatted as prefix + zero-padded number.

    Example:
        >>> vendors = generate_vendor_ids(5)
        >>> vendors
        ['V00001', 'V00002', 'V00003', 'V00004', 'V00005']
    """
    return [f"{prefix}{i:05d}" for i in range(1, count + 1)]


def generate_department_names() -> List[str]:
    """
    Generate a list of department names for General Ledger.

    Returns:
        A list of realistic department names.

    Example:
        >>> depts = generate_department_names()
        >>> 'Sales' in depts
        True
    """
    return [
        "Accounting",
        "Sales",
        "Marketing",
        "Operations",
        "Finance",
        "Human Resources",
        "IT",
        "Legal",
        "Procurement",
        "Logistics"
    ]


def generate_invoice_numbers(
    count: int,
    seed: int | None = None
) -> List[str]:
    """
    Generate a list of invoice numbers.

    Args:
        count: Number of invoice numbers to generate.
        seed: Random seed for reproducibility.

    Returns:
        A list of invoice numbers formatted as INV + zero-padded number.

    Example:
        >>> invoices = generate_invoice_numbers(5, seed=42)
        >>> len(invoices)
        5
    """
    if seed is not None:
        random.seed(seed)

    return [f"INV{random.randint(100000, 999999):06d}" for _ in range(count)]


def generate_status_list(
    count: int,
    distribution: dict | None = None,
    seed: int | None = None
) -> List[str]:
    """
    Generate a list of transaction statuses with realistic distribution.

    Args:
        count: Number of statuses to generate.
        distribution: Dict with status as key and percentage (0-1) as value.
                     Default: {'paid': 0.7, 'pending': 0.2, 'disputed': 0.1}
        seed: Random seed for reproducibility.

    Returns:
        A list of status strings with specified distribution.

    Raises:
        ValueError: If distribution values don't sum to 1.0.

    Example:
        >>> statuses = generate_status_list(100, seed=42)
        >>> len(statuses)
        100
    """
    if seed is not None:
        random.seed(seed)

    if distribution is None:
        distribution = {'paid': 0.7, 'pending': 0.2, 'disputed': 0.1}

    # Validate distribution sums to 1.0 (with tolerance for floating point)
    total = sum(distribution.values())
    if not (0.99 <= total <= 1.01):
        raise ValueError(f"Distribution values must sum to 1.0, got {total}")

    statuses = []
    for status, pct in distribution.items():
        statuses.extend([status] * int(count * pct))

    # Handle rounding by filling remaining with first status
    if len(statuses) < count:
        statuses.extend([list(distribution.keys())[0]] * (count - len(statuses)))

    random.shuffle(statuses)
    return statuses[:count]
