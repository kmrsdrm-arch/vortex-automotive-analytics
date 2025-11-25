"""Data formatting utilities."""


def format_currency(value: float) -> str:
    """Format number as currency."""
    return f"${value:,.2f}"


def format_number(value: int) -> str:
    """Format number with thousands separator."""
    return f"{value:,}"


def format_percentage(value: float) -> str:
    """Format number as percentage."""
    return f"{value:.2f}%"


def format_change(current: float, previous: float) -> str:
    """Format percentage change."""
    if previous == 0:
        return "N/A"
    change = ((current - previous) / previous) * 100
    sign = "+" if change > 0 else ""
    return f"{sign}{change:.2f}%"

