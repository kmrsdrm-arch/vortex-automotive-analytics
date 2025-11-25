"""Analytics endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date, datetime, timedelta

from src.api.dependencies import get_db
from src.analytics.sales_analytics import SalesAnalytics
from src.analytics.inventory_analytics import InventoryAnalytics
from src.analytics.kpi_calculator import KPICalculator
from src.analytics.trend_analyzer import TrendAnalyzer

router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics"])


@router.get("/sales/summary")
async def get_sales_summary(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    """Get sales summary for a period."""
    analytics = SalesAnalytics(db)
    return analytics.get_sales_summary(start_date, end_date)


@router.get("/sales/trends")
async def get_sales_trends(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    period: str = Query("D", description="D=daily, W=weekly, M=monthly"),
    db: Session = Depends(get_db),
):
    """Get sales trends over time."""
    analytics = SalesAnalytics(db)
    return analytics.get_sales_trends(start_date, end_date, period)


@router.get("/sales/regional")
async def get_regional_performance(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    """Get sales performance by region."""
    analytics = SalesAnalytics(db)
    return analytics.get_regional_performance(start_date, end_date)


@router.get("/sales/top-vehicles")
async def get_top_selling_vehicles(
    n: int = Query(10, description="Number of top vehicles"),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    """Get top N selling vehicles."""
    analytics = SalesAnalytics(db)
    return analytics.get_top_selling_vehicles(n, start_date, end_date)


@router.get("/sales/categories")
async def get_category_breakdown(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    """Get sales breakdown by vehicle category."""
    analytics = SalesAnalytics(db)
    return analytics.get_category_breakdown(start_date, end_date)


@router.get("/sales/segments")
async def get_customer_segment_analysis(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    """Get sales analysis by customer segment."""
    analytics = SalesAnalytics(db)
    return analytics.get_customer_segment_analysis(start_date, end_date)


@router.get("/inventory/summary")
async def get_inventory_summary(db: Session = Depends(get_db)):
    """Get overall inventory summary."""
    analytics = InventoryAnalytics(db)
    return analytics.get_inventory_summary()


@router.get("/inventory/status")
async def get_inventory_status(db: Session = Depends(get_db)):
    """Get current inventory levels and status."""
    analytics = InventoryAnalytics(db)
    return {
        "summary": analytics.get_inventory_summary(),
        "by_region": analytics.get_inventory_by_region(),
        "by_category": analytics.get_inventory_by_category(),
    }


@router.get("/inventory/by-status")
async def get_inventory_by_status(db: Session = Depends(get_db)):
    """Get inventory breakdown by status."""
    analytics = InventoryAnalytics(db)
    return analytics.get_inventory_by_status()


@router.get("/inventory/low-stock")
async def get_low_stock_alerts(db: Session = Depends(get_db)):
    """Get vehicles with low stock levels."""
    analytics = InventoryAnalytics(db)
    return analytics.get_low_stock_alerts()


@router.get("/inventory/turnover")
async def get_inventory_turnover(db: Session = Depends(get_db)):
    """Get inventory turnover metrics."""
    analytics = InventoryAnalytics(db)
    return {
        "summary": analytics.get_inventory_summary(),
        "warehouse_utilization": analytics.get_warehouse_utilization(),
    }


@router.get("/kpis")
async def get_kpis(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    """Get key performance indicators."""
    calculator = KPICalculator(db)
    return calculator.calculate_all_kpis(start_date, end_date)


@router.get("/kpis/comparison")
async def get_kpis_comparison(
    days: int = Query(30, description="Number of days in current period"),
    db: Session = Depends(get_db),
):
    """Get KPIs with period-over-period comparison."""
    calculator = KPICalculator(db)
    return calculator.calculate_period_comparison(days)


@router.get("/trends/anomalies")
async def detect_anomalies(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    """Detect anomalies in sales data."""
    analyzer = TrendAnalyzer(db)
    return analyzer.detect_sales_anomalies(start_date, end_date)


@router.get("/trends/moving-average")
async def get_moving_average(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    window: int = Query(7, description="Moving average window size"),
    db: Session = Depends(get_db),
):
    """Calculate moving average for sales."""
    analyzer = TrendAnalyzer(db)
    return analyzer.calculate_moving_average(start_date, end_date, window)


@router.get("/trends/forecast")
async def get_forecast(
    days_ahead: int = Query(7, description="Number of days to forecast"),
    historical_days: int = Query(30, description="Days of historical data to use"),
    db: Session = Depends(get_db),
):
    """Get sales forecast."""
    analyzer = TrendAnalyzer(db)
    return analyzer.forecast_simple(days_ahead, historical_days)

