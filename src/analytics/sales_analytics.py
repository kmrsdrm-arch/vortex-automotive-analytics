"""Sales-specific analytics functions."""

import pandas as pd
from typing import Dict, Any, Optional, List
from datetime import date, timedelta, datetime
from sqlalchemy.orm import Session

from src.pipeline.extractors.data_extractor import DataExtractor
from src.pipeline.transformers.aggregator import DataAggregator
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SalesAnalytics:
    """Sales analytics calculator."""

    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db
        self.extractor = DataExtractor(db)
        self.aggregator = DataAggregator()

    def get_sales_summary(
        self, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Get sales summary for a period."""
        try:
            df = self.extractor.extract_sales(start_date, end_date)

            if df.empty:
                return {
                    "total_revenue": 0,
                    "total_units": 0,
                    "total_transactions": 0,
                    "avg_transaction_value": 0,
                    "avg_discount": 0,
                }

            summary = {
                "total_revenue": float(df["total_amount"].sum()),
                "total_units": int(df["quantity"].sum()),
                "total_transactions": len(df),
                "avg_transaction_value": float(df["total_amount"].mean()),
                "avg_discount": float(df["discount_applied"].mean()),
                "period_start": str(start_date) if start_date else None,
                "period_end": str(end_date) if end_date else None,
            }

            logger.info(f"Generated sales summary: {summary['total_revenue']} revenue")
            return summary

        except Exception as e:
            logger.error(f"Error generating sales summary: {e}")
            raise

    def get_sales_trends(
        self, start_date: Optional[date] = None, end_date: Optional[date] = None, period: str = "D"
    ) -> List[Dict[str, Any]]:
        """Get sales trends over time."""
        try:
            df = self.extractor.extract_sales(start_date, end_date)

            if df.empty:
                return []

            trends_df = self.aggregator.aggregate_sales_by_period(df, period)
            trends = trends_df.to_dict(orient="records")

            logger.info(f"Generated {len(trends)} sales trend records")
            return trends

        except Exception as e:
            logger.error(f"Error generating sales trends: {e}")
            raise

    def get_regional_performance(
        self, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Get sales performance by region."""
        try:
            df = self.extractor.extract_sales(start_date, end_date)

            if df.empty:
                return []

            regional_df = self.aggregator.aggregate_sales_by_region(df)
            regional = regional_df.to_dict(orient="records")

            logger.info(f"Generated regional performance for {len(regional)} regions")
            return regional

        except Exception as e:
            logger.error(f"Error generating regional performance: {e}")
            raise

    def get_top_selling_vehicles(
        self, n: int = 10, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Get top N selling vehicles."""
        try:
            df = self.extractor.extract_sales_with_vehicle_info(start_date, end_date)

            if df.empty:
                return []

            top_vehicles_df = self.aggregator.aggregate_top_n_vehicles(df, n)
            top_vehicles = top_vehicles_df.to_dict(orient="records")

            logger.info(f"Generated top {n} selling vehicles")
            return top_vehicles

        except Exception as e:
            logger.error(f"Error generating top selling vehicles: {e}")
            raise

    def get_category_breakdown(
        self, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Get sales breakdown by vehicle category."""
        try:
            df = self.extractor.extract_sales_with_vehicle_info(start_date, end_date)

            if df.empty:
                return []

            category_df = self.aggregator.aggregate_sales_by_category(df)
            categories = category_df.to_dict(orient="records")

            logger.info(f"Generated category breakdown for {len(categories)} categories")
            return categories

        except Exception as e:
            logger.error(f"Error generating category breakdown: {e}")
            raise

    def get_customer_segment_analysis(
        self, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Get sales analysis by customer segment."""
        try:
            df = self.extractor.extract_sales(start_date, end_date)

            if df.empty:
                return []

            segment_df = self.aggregator.aggregate_sales_by_customer_segment(df)
            segments = segment_df.to_dict(orient="records")

            logger.info(f"Generated customer segment analysis for {len(segments)} segments")
            return segments

        except Exception as e:
            logger.error(f"Error generating customer segment analysis: {e}")
            raise

    def compare_periods(
        self, current_start: date, current_end: date, previous_start: date, previous_end: date
    ) -> Dict[str, Any]:
        """Compare two time periods."""
        try:
            current = self.get_sales_summary(current_start, current_end)
            previous = self.get_sales_summary(previous_start, previous_end)

            comparison = {
                "current_period": current,
                "previous_period": previous,
                "revenue_change": current["total_revenue"] - previous["total_revenue"],
                "revenue_change_pct": (
                    (current["total_revenue"] - previous["total_revenue"])
                    / previous["total_revenue"]
                    * 100
                    if previous["total_revenue"] > 0
                    else 0
                ),
                "units_change": current["total_units"] - previous["total_units"],
                "units_change_pct": (
                    (current["total_units"] - previous["total_units"])
                    / previous["total_units"]
                    * 100
                    if previous["total_units"] > 0
                    else 0
                ),
            }

            logger.info(f"Compared periods: {comparison['revenue_change_pct']:.2f}% revenue change")
            return comparison

        except Exception as e:
            logger.error(f"Error comparing periods: {e}")
            raise

