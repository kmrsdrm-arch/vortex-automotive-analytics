"""KPI calculation functions."""

from typing import Dict, Any, Optional
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session

from src.analytics.sales_analytics import SalesAnalytics
from src.analytics.inventory_analytics import InventoryAnalytics
from src.utils.logger import get_logger

logger = get_logger(__name__)


class KPICalculator:
    """Calculate key performance indicators."""

    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db
        self.sales_analytics = SalesAnalytics(db)
        self.inventory_analytics = InventoryAnalytics(db)

    def calculate_all_kpis(
        self, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Calculate all KPIs for a period."""
        try:
            # Default to last 30 days
            if not end_date:
                end_date = datetime.now().date()
            if not start_date:
                start_date = end_date - timedelta(days=30)

            # Sales KPIs
            sales_summary = self.sales_analytics.get_sales_summary(start_date, end_date)

            # Inventory KPIs
            inventory_summary = self.inventory_analytics.get_inventory_summary()

            # Calculate additional KPIs
            days_in_period = (end_date - start_date).days + 1
            avg_daily_revenue = sales_summary["total_revenue"] / days_in_period if days_in_period > 0 else 0

            # Inventory turnover approximation (units sold / average inventory)
            turnover_rate = (
                sales_summary["total_units"] / inventory_summary["total_units"]
                if inventory_summary["total_units"] > 0
                else 0
            )

            kpis = {
                # Revenue KPIs
                "total_revenue": sales_summary["total_revenue"],
                "avg_daily_revenue": avg_daily_revenue,
                "avg_transaction_value": sales_summary["avg_transaction_value"],
                # Sales Volume KPIs
                "total_units_sold": sales_summary["total_units"],
                "total_transactions": sales_summary["total_transactions"],
                "avg_units_per_transaction": (
                    sales_summary["total_units"] / sales_summary["total_transactions"]
                    if sales_summary["total_transactions"] > 0
                    else 0
                ),
                # Discount KPIs
                "avg_discount_pct": sales_summary["avg_discount"],
                # Inventory KPIs
                "total_inventory_units": inventory_summary["total_units"],
                "total_inventory_value": inventory_summary["total_value"],
                "inventory_turnover_rate": turnover_rate,
                "low_stock_items": inventory_summary["low_stock_count"],
                "out_of_stock_items": inventory_summary["out_of_stock_count"],
                # Operational KPIs
                "stock_availability_rate": (
                    (inventory_summary["active_count"] + inventory_summary["low_stock_count"])
                    / (
                        inventory_summary["active_count"]
                        + inventory_summary["low_stock_count"]
                        + inventory_summary["out_of_stock_count"]
                    )
                    * 100
                    if (
                        inventory_summary["active_count"]
                        + inventory_summary["low_stock_count"]
                        + inventory_summary["out_of_stock_count"]
                    )
                    > 0
                    else 0
                ),
                # Period info
                "period_start": str(start_date),
                "period_end": str(end_date),
                "period_days": days_in_period,
            }

            logger.info(f"Calculated all KPIs for period {start_date} to {end_date}")
            return kpis

        except Exception as e:
            logger.error(f"Error calculating KPIs: {e}")
            raise

    def calculate_period_comparison(
        self, current_days: int = 30, compare_to_previous: bool = True
    ) -> Dict[str, Any]:
        """Calculate KPIs with period-over-period comparison."""
        try:
            end_date = datetime.now().date()
            current_start = end_date - timedelta(days=current_days - 1)

            previous_end = current_start - timedelta(days=1)
            previous_start = previous_end - timedelta(days=current_days - 1)

            current_kpis = self.calculate_all_kpis(current_start, end_date)
            previous_kpis = self.calculate_all_kpis(previous_start, previous_end)

            # Calculate changes
            revenue_change_pct = (
                (current_kpis["total_revenue"] - previous_kpis["total_revenue"])
                / previous_kpis["total_revenue"]
                * 100
                if previous_kpis["total_revenue"] > 0
                else 0
            )

            units_change_pct = (
                (current_kpis["total_units_sold"] - previous_kpis["total_units_sold"])
                / previous_kpis["total_units_sold"]
                * 100
                if previous_kpis["total_units_sold"] > 0
                else 0
            )

            comparison = {
                "current_period": current_kpis,
                "previous_period": previous_kpis,
                "changes": {
                    "revenue_change_pct": revenue_change_pct,
                    "units_change_pct": units_change_pct,
                    "avg_transaction_value_change_pct": (
                        (
                            current_kpis["avg_transaction_value"]
                            - previous_kpis["avg_transaction_value"]
                        )
                        / previous_kpis["avg_transaction_value"]
                        * 100
                        if previous_kpis["avg_transaction_value"] > 0
                        else 0
                    ),
                },
            }

            logger.info(f"Calculated period comparison: {revenue_change_pct:.2f}% revenue change")
            return comparison

        except Exception as e:
            logger.error(f"Error calculating period comparison: {e}")
            raise

