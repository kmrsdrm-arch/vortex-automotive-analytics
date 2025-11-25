"""Report generation endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse, HTMLResponse
from sqlalchemy.orm import Session

from src.api.dependencies import get_db
from src.api.schemas.requests import ReportGenerationRequest
from src.api.schemas.responses import ReportResponse
from src.llm.services.report_service import ReportService

router = APIRouter(prefix="/api/v1/reports", tags=["Reports"])


@router.post("/generate", response_model=ReportResponse)
async def generate_report(request: ReportGenerationRequest, db: Session = Depends(get_db)):
    """Generate a report."""
    try:
        service = ReportService(db)

        if request.report_type == "executive":
            report = service.generate_executive_report(request.start_date, request.end_date)
        elif request.report_type == "detailed":
            report = service.generate_detailed_report(request.start_date, request.end_date)
        elif request.report_type == "product":
            if not request.vehicle_id:
                raise HTTPException(status_code=400, detail="vehicle_id required for product reports")
            report = service.generate_product_report(
                request.vehicle_id, request.start_date, request.end_date
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unknown report type: {request.report_type}")

        return ReportResponse(**report)
    except HTTPException:
        raise
    except Exception as e:
        from src.utils.logger import get_logger
        logger = get_logger(__name__)
        logger.error(f"Error in generate_report endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")


@router.post("/generate/markdown", response_class=PlainTextResponse)
async def generate_report_markdown(request: ReportGenerationRequest, db: Session = Depends(get_db)):
    """Generate a report in Markdown format."""
    service = ReportService(db)

    if request.report_type == "executive":
        report = service.generate_executive_report(request.start_date, request.end_date)
    elif request.report_type == "detailed":
        report = service.generate_detailed_report(request.start_date, request.end_date)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown report type: {request.report_type}")

    return service.export_report_markdown(report)


@router.post("/generate/html", response_class=HTMLResponse)
async def generate_report_html(request: ReportGenerationRequest, db: Session = Depends(get_db)):
    """Generate a report in HTML format."""
    service = ReportService(db)

    if request.report_type == "executive":
        report = service.generate_executive_report(request.start_date, request.end_date)
    elif request.report_type == "detailed":
        report = service.generate_detailed_report(request.start_date, request.end_date)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown report type: {request.report_type}")

    return service.export_report_html(report)

