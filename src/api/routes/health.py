"""Health check endpoints."""

from fastapi import APIRouter
from datetime import datetime
from src.api.schemas.common import HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy", message="Automotive Analytics API is running", timestamp=datetime.now().isoformat()
    )

