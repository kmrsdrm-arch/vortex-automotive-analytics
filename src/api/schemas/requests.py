"""Request schemas."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class NLQueryRequest(BaseModel):
    """Natural language query request."""

    question: str = Field(..., description="Natural language question")
    context: Optional[str] = Field(None, description="Additional context")


class InsightsGenerationRequest(BaseModel):
    """Insights generation request."""

    start_date: Optional[date] = None
    end_date: Optional[date] = None
    focus_area: str = Field(default="sales", description="Focus area: sales, inventory, or general")


class ReportGenerationRequest(BaseModel):
    """Report generation request."""

    report_type: str = Field(..., description="Report type: executive, detailed, or product")
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    vehicle_id: Optional[int] = Field(None, description="Vehicle ID for product reports")
    params: Optional[dict] = Field(default_factory=dict, description="Additional parameters")


class RAGQueryRequest(BaseModel):
    """RAG query request."""

    question: str = Field(..., description="Question to answer")
    context_limit: int = Field(default=3, description="Number of context items to use")

