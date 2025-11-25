"""Common schemas."""

from pydantic import BaseModel
from typing import Optional
from datetime import date


class DateRangeFilter(BaseModel):
    """Date range filter."""

    start_date: Optional[date] = None
    end_date: Optional[date] = None


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    message: str
    timestamp: str

