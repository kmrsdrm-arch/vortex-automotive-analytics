"""Trend analysis functions."""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session

from src.pipeline.extractors.data_extractor import DataExtractor
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TrendAnalyzer:
    """Analyze trends in sales and inventory data."""

    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db
        self.extractor = DataExtractor(db)

    def detect_sales_anomalies(
        self, start_date: Optional[date] = None, end_date: Optional[date] = None, threshold: float = 2.0
    ) -> List[Dict[str, Any]]:
        """Detect anomalies in daily sales using z-score."""
        try:
            df = self.extractor.extract_sales(start_date, end_date)

            if df.empty or len(df) < 7:  # Need minimum data
                logger.warning("Insufficient data for anomaly detection")
                return []

            # Aggregate by day
            daily_sales = (
                df.groupby("sale_date")
                .agg({"total_amount": "sum", "quantity": "sum"})
                .reset_index()
            )

            # Calculate z-scores
            daily_sales["revenue_zscore"] = (
                daily_sales["total_amount"] - daily_sales["total_amount"].mean()
            ) / daily_sales["total_amount"].std()

            # Find anomalies
            anomalies_df = daily_sales[np.abs(daily_sales["revenue_zscore"]) > threshold]

            anomalies = [
                {
                    "date": str(row["sale_date"]),
                    "revenue": float(row["total_amount"]),
                    "units": int(row["quantity"]),
                    "zscore": float(row["revenue_zscore"]),
                    "type": "high" if row["revenue_zscore"] > 0 else "low",
                }
                for _, row in anomalies_df.iterrows()
            ]

            logger.info(f"Detected {len(anomalies)} sales anomalies")
            return anomalies

        except Exception as e:
            logger.error(f"Error detecting sales anomalies: {e}")
            raise

    def calculate_moving_average(
        self, start_date: Optional[date] = None, end_date: Optional[date] = None, window: int = 7
    ) -> List[Dict[str, Any]]:
        """Calculate moving average for sales."""
        try:
            df = self.extractor.extract_sales(start_date, end_date)

            if df.empty:
                return []

            # Aggregate by day
            daily_sales = (
                df.groupby("sale_date").agg({"total_amount": "sum"}).reset_index().sort_values("sale_date")
            )

            # Calculate moving average
            daily_sales["moving_avg"] = (
                daily_sales["total_amount"].rolling(window=window, min_periods=1).mean()
            )

            result = [
                {
                    "date": str(row["sale_date"]),
                    "actual_revenue": float(row["total_amount"]),
                    "moving_avg": float(row["moving_avg"]),
                }
                for _, row in daily_sales.iterrows()
            ]

            logger.info(f"Calculated {window}-day moving average for {len(result)} days")
            return result

        except Exception as e:
            logger.error(f"Error calculating moving average: {e}")
            raise

    def forecast_simple(
        self, days_ahead: int = 7, historical_days: int = 30
    ) -> List[Dict[str, Any]]:
        """Simple forecast based on historical average (naive approach)."""
        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=historical_days)

            df = self.extractor.extract_sales(start_date, end_date)

            if df.empty:
                return []

            # Calculate daily average
            daily_avg = df.groupby("sale_date")["total_amount"].sum().mean()

            # Generate forecast
            forecast = []
            for i in range(1, days_ahead + 1):
                forecast_date = end_date + timedelta(days=i)
                # Add some random variation (±10%)
                variation = np.random.uniform(0.9, 1.1)
                forecast.append(
                    {
                        "date": str(forecast_date),
                        "forecasted_revenue": float(daily_avg * variation),
                        "confidence": "low",  # Naive forecast has low confidence
                    }
                )

            logger.info(f"Generated {days_ahead}-day forecast")
            return forecast

        except Exception as e:
            logger.error(f"Error generating forecast: {e}")
            raise

    def identify_seasonal_patterns(
        self, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Identify seasonal patterns in sales."""
        try:
            df = self.extractor.extract_sales(start_date, end_date)

            if df.empty:
                return {}

            df["sale_date"] = pd.to_datetime(df["sale_date"])
            df["month"] = df["sale_date"].dt.month
            df["day_of_week"] = df["sale_date"].dt.dayofweek

            # Monthly pattern
            monthly_avg = df.groupby("month")["total_amount"].mean().to_dict()
            monthly_avg = {int(k): float(v) for k, v in monthly_avg.items()}

            # Day of week pattern
            dow_avg = df.groupby("day_of_week")["total_amount"].mean().to_dict()
            dow_avg = {int(k): float(v) for k, v in dow_avg.items()}

            patterns = {"monthly_pattern": monthly_avg, "day_of_week_pattern": dow_avg}

            logger.info("Identified seasonal patterns")
            return patterns

        except Exception as e:
            logger.error(f"Error identifying seasonal patterns: {e}")
            raise

