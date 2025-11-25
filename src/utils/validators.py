"""Data validation utilities."""

from datetime import datetime
from typing import Any, Optional


def validate_date_range(start_date: Optional[datetime], end_date: Optional[datetime]) -> bool:
    """Validate that start_date is before end_date."""
    if start_date and end_date:
        return start_date <= end_date
    return True


def validate_positive_number(value: Any) -> bool:
    """Validate that a value is a positive number."""
    try:
        num = float(value)
        return num > 0
    except (ValueError, TypeError):
        return False


def validate_non_negative_number(value: Any) -> bool:
    """Validate that a value is a non-negative number."""
    try:
        num = float(value)
        return num >= 0
    except (ValueError, TypeError):
        return False

