"""General helper functions."""

from datetime import datetime, timedelta
from typing import List, Tuple


def get_date_range(days: int = 30) -> Tuple[datetime, datetime]:
    """Get a date range for the last N days."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def format_currency(amount: float) -> str:
    """Format a number as currency."""
    return f"${amount:,.2f}"


def format_percentage(value: float) -> str:
    """Format a number as percentage."""
    return f"{value:.2f}%"


def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """Split a list into chunks of specified size."""
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]

