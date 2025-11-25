"""Response schemas."""

from pydantic import BaseModel
from typing import Any, List, Optional, Dict
from datetime import datetime


class NLQueryResponse(BaseModel):
    """Natural language query response."""

    success: bool
    question: str
    sql: Optional[str] = None
    results: Optional[Any] = None
    explanation: Optional[str] = None
    row_count: Optional[int] = None
    error: Optional[str] = None


class InsightResponse(BaseModel):
    """Single insight response."""

    text: str
    type: str
    metadata: Optional[Dict[str, Any]] = None


class InsightsResponse(BaseModel):
    """Insights generation response."""

    insights: List[InsightResponse]
    focus_area: str
    generated_at: str


class ReportResponse(BaseModel):
    """Report generation response."""

    report_id: Optional[int] = None
    report_type: str
    report_title: str
    content: str
    generated_at: str
    period_start: Optional[str] = None
    period_end: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response."""

    error: str
    detail: Optional[str] = None
    timestamp: str

