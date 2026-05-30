"""Helper functions for synthetic financial data generation.

Provides reusable utilities for generating realistic financial data.
Callers are responsible for seeding random state before calling these functions.
"""

import random
from datetime import datetime, timedelta
from typing import List


def generate_random_date(start_date: datetime, end_date: datetime) -> datetime:
    """
    Generate a random datetime between start_date and end_date.

    Caller must seed random state before calling in a loop to ensure
    different values per iteration.

    Args:
        start_date: The earliest possible datetime.
        end_date: The latest possible datetime.

    Returns:
        A random datetime object between start_date and end_date.

    Raises:
        ValueError: If start_date is after end_date.

    Example:
        >>> random.seed(42)
        >>> start = datetime(2026, 1, 1)
        >>> end = datetime(2026, 3, 31)
        >>> date = generate_random_date(start, end)
        >>> start <= date <= end
        True
    """
    if start_date > end_date:
        raise ValueError("start_date must be before or equal to end_date")

    time_delta = end_date - start_date
    random_seconds = random.randint(0, int(time_delta.total_seconds()))
    return start_date + timedelta(seconds=random_seconds)


def generate_random_amount(
    min_amount: float,
    max_amount: float,
    decimal_places: int = 2,
) -> float:
    """
    Generate a random amount between min_amount and max_amount.

    Uses a weighted distribution to produce realistic financial amounts
    (more small transactions, fewer large ones).

    Caller must seed random state before calling in a loop to ensure
    different values per iteration.

    Args:
        min_amount: Minimum amount value.
        max_amount: Maximum amount value.
        decimal_places: Number of decimal places to round to.

    Returns:
        A random float amount with specified decimal places.

    Raises:
        ValueError: If min_amount is negative or greater than max_amount.

    Example:
        >>> random.seed(42)
        >>> amount = generate_random_amount(100, 50000)
        >>> 100 <= amount <= 50000
        True
    """
    if min_amount < 0:
        raise ValueError("min_amount must be non-negative")
    if min_amount > max_amount:
        raise ValueError("min_amount must be less than or equal to max_amount")

    random_value = random.random()
    amount = min_amount + (max_amount - min_amount) * (random_value ** 0.7)
    return round(amount, decimal_places)


def generate_vendor_ids(count: int, prefix: str = "V") -> List[str]:
    """
    Generate a list of vendor IDs.

    Args:
        count: Number of vendor IDs to generate.
        prefix: Prefix for vendor IDs (default: "V").

    Returns:
        A list of vendor IDs formatted as prefix + zero-padded number.

    Example:
        >>> generate_vendor_ids(3, prefix="VENDOR")
        ['VENDOR00001', 'VENDOR00002', 'VENDOR00003']
    """
    return [f"{prefix}{i:05d}" for i in range(1, count + 1)]


def generate_department_names() -> List[str]:
    """
    Generate a list of department names for General Ledger cost centers.

    Returns:
        A list of realistic department names.

    Example:
        >>> depts = generate_department_names()
        >>> "Finance" in depts
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
        "Logistics",
    ]


def generate_invoice_numbers(count: int) -> List[str]:
    """
    Generate a list of invoice numbers.

    Caller must seed random state beforehand for reproducibility.

    Args:
        count: Number of invoice numbers to generate.

    Returns:
        A list of invoice numbers formatted as INV + 6-digit number.

    Example:
        >>> random.seed(42)
        >>> invoices = generate_invoice_numbers(3)
        >>> all(inv.startswith("INV") for inv in invoices)
        True
    """
    return [f"INV{random.randint(100000, 999999):06d}" for _ in range(count)]


def generate_status_list(
    count: int,
    distribution: dict | None = None,
) -> List[str]:
    """
    Generate a list of transaction statuses with realistic distribution.

    Caller must seed random state beforehand for reproducibility.

    Args:
        count: Number of statuses to generate.
        distribution: Dict mapping status to percentage (0-1).
            Default: {'paid': 0.7, 'pending': 0.2, 'disputed': 0.1}

    Returns:
        A shuffled list of status strings matching the specified distribution.

    Raises:
        ValueError: If distribution values don't sum to approximately 1.0.

    Example:
        >>> random.seed(42)
        >>> statuses = generate_status_list(100)
        >>> len(statuses)
        100
    """
    if distribution is None:
        distribution = {"paid": 0.7, "pending": 0.2, "disputed": 0.1}

    total = sum(distribution.values())
    if not (0.99 <= total <= 1.01):
        raise ValueError(f"Distribution values must sum to 1.0, got {total}")

    statuses = []
    for status, pct in distribution.items():
        statuses.extend([status] * int(count * pct))

    if len(statuses) < count:
        statuses.extend([list(distribution.keys())[0]] * (count - len(statuses)))

    random.shuffle(statuses)
    return statuses[:count]
