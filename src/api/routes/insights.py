"""Insights endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from src.api.dependencies import get_db
from src.api.schemas.requests import InsightsGenerationRequest
from src.api.schemas.responses import InsightsResponse, InsightResponse
from src.llm.services.insights_service import InsightsService

router = APIRouter(prefix="/api/v1/insights", tags=["Insights"])


@router.post("/generate", response_model=InsightsResponse)
async def generate_insights(request: InsightsGenerationRequest, db: Session = Depends(get_db)):
    """Generate AI-powered insights."""
    try:
        service = InsightsService(db)

        if request.focus_area == "sales":
            insights_list = service.generate_sales_insights(request.start_date, request.end_date)
        elif request.focus_area == "inventory":
            insights_list = service.generate_inventory_insights()
        else:
            # Generate both
            sales_insights = service.generate_sales_insights(request.start_date, request.end_date)
            inventory_insights = service.generate_inventory_insights()
            insights_list = sales_insights + inventory_insights

        insights = [
            InsightResponse(text=i["text"], type=i["type"], metadata=i.get("metadata"))
            for i in insights_list
        ]

        return InsightsResponse(
            insights=insights, focus_area=request.focus_area, generated_at=datetime.now().isoformat()
        )
    except Exception as e:
        from src.utils.logger import get_logger
        logger = get_logger(__name__)
        logger.error(f"Error in generate_insights endpoint: {e}")
        # Return empty insights with error message
        return InsightsResponse(
            insights=[InsightResponse(text=f"Error generating insights: {str(e)}", type="error", metadata={})],
            focus_area=request.focus_area,
            generated_at=datetime.now().isoformat()
        )


@router.get("/anomalies")
async def analyze_anomalies(db: Session = Depends(get_db)):
    """Analyze and explain anomalies."""
    service = InsightsService(db)
    return service.analyze_anomalies()


@router.get("/trends")
async def analyze_trends(db: Session = Depends(get_db)):
    """Analyze sales trends."""
    service = InsightsService(db)
    return service.analyze_trends()


@router.get("/history")
async def get_insight_history(limit: int = 50, db: Session = Depends(get_db)):
    """Get historical insights."""
    from src.database.models import InsightHistory

    insights = db.query(InsightHistory).order_by(InsightHistory.generated_at.desc()).limit(limit).all()

    return [
        {
            "id": i.id,
            "text": i.insight_text,
            "type": i.insight_type,
            "generated_at": i.generated_at.isoformat(),
            "metadata": i.insight_metadata,
        }
        for i in insights
    ]

