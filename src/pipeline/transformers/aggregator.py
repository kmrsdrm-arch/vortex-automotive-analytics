"""Data aggregation logic."""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DataAggregator:
    """Aggregate data for analytics."""

    @staticmethod
    def aggregate_sales_by_period(
        df: pd.DataFrame, period: str = "D", date_column: str = "sale_date"
    ) -> pd.DataFrame:
        """Aggregate sales by time period (D=daily, W=weekly, M=monthly)."""
        try:
            df[date_column] = pd.to_datetime(df[date_column])
            df_agg = (
                df.groupby(pd.Grouper(key=date_column, freq=period))
                .agg(
                    {
                        "quantity": "sum",
                        "total_amount": "sum",
                        "id": "count",  # transaction count
                    }
                )
                .rename(columns={"id": "transaction_count"})
                .reset_index()
            )

            df_agg["avg_transaction_value"] = (
                df_agg["total_amount"] / df_agg["transaction_count"]
            )

            logger.info(f"Aggregated sales by {period}")
            return df_agg

        except Exception as e:
            logger.error(f"Error aggregating sales by period: {e}")
            raise

    @staticmethod
    def aggregate_sales_by_region(df: pd.DataFrame) -> pd.DataFrame:
        """Aggregate sales by region."""
        try:
            df_agg = (
                df.groupby("region")
                .agg(
                    {
                        "quantity": "sum",
                        "total_amount": "sum",
                        "id": "count",
                        "discount_applied": "mean",
                    }
                )
                .rename(columns={"id": "transaction_count"})
                .reset_index()
            )

            df_agg["avg_sale_amount"] = df_agg["total_amount"] / df_agg["transaction_count"]

            logger.info(f"Aggregated sales by region")
            return df_agg

        except Exception as e:
            logger.error(f"Error aggregating sales by region: {e}")
            raise

    @staticmethod
    def aggregate_sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
        """Aggregate sales by vehicle category."""
        try:
            if "category" not in df.columns:
                logger.warning("Category column not found in dataframe")
                return pd.DataFrame()

            df_agg = (
                df.groupby("category")
                .agg({"quantity": "sum", "total_amount": "sum", "sale_id": "count"})
                .rename(columns={"sale_id": "transaction_count"})
                .reset_index()
            )

            df_agg["avg_unit_price"] = df_agg["total_amount"] / df_agg["quantity"]

            logger.info(f"Aggregated sales by category")
            return df_agg

        except Exception as e:
            logger.error(f"Error aggregating sales by category: {e}")
            raise

    @staticmethod
    def aggregate_sales_by_customer_segment(df: pd.DataFrame) -> pd.DataFrame:
        """Aggregate sales by customer segment."""
        try:
            df_agg = (
                df.groupby("customer_segment")
                .agg(
                    {
                        "quantity": "sum",
                        "total_amount": "sum",
                        "id": "count",
                        "discount_applied": "mean",
                    }
                )
                .rename(columns={"id": "transaction_count"})
                .reset_index()
            )

            df_agg["avg_quantity_per_transaction"] = (
                df_agg["quantity"] / df_agg["transaction_count"]
            )

            logger.info(f"Aggregated sales by customer segment")
            return df_agg

        except Exception as e:
            logger.error(f"Error aggregating sales by customer segment: {e}")
            raise

    @staticmethod
    def aggregate_top_n_vehicles(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
        """Get top N vehicles by sales."""
        try:
            if "vehicle_id" not in df.columns:
                logger.warning("vehicle_id column not found")
                return pd.DataFrame()

            df_agg = (
                df.groupby(["vehicle_id", "make", "model", "category"])
                .agg({"quantity": "sum", "total_amount": "sum"})
                .reset_index()
                .sort_values("total_amount", ascending=False)
                .head(n)
            )

            logger.info(f"Aggregated top {n} vehicles")
            return df_agg

        except Exception as e:
            logger.error(f"Error aggregating top vehicles: {e}")
            raise

    @staticmethod
    def aggregate_inventory_by_status(df: pd.DataFrame) -> pd.DataFrame:
        """Aggregate inventory by status."""
        try:
            df_agg = (
                df.groupby("status")
                .agg(
                    {
                        "inventory_id": "count",
                        "quantity_available": "sum",
                        "quantity_reserved": "sum",
                    }
                )
                .rename(columns={"inventory_id": "record_count"})
                .reset_index()
            )

            logger.info(f"Aggregated inventory by status")
            return df_agg

        except Exception as e:
            logger.error(f"Error aggregating inventory by status: {e}")
            raise

    @staticmethod
    def calculate_inventory_turnover(
        sales_df: pd.DataFrame, inventory_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Calculate inventory turnover rate."""
        try:
            # Get sales by vehicle
            sales_by_vehicle = (
                sales_df.groupby("vehicle_id").agg({"quantity": "sum"}).reset_index()
            )
            sales_by_vehicle.rename(columns={"quantity": "total_sold"}, inplace=True)

            # Get average inventory by vehicle
            inv_by_vehicle = (
                inventory_df.groupby("vehicle_id")
                .agg({"quantity_available": "sum"})
                .reset_index()
            )
            inv_by_vehicle.rename(columns={"quantity_available": "avg_inventory"}, inplace=True)

            # Merge and calculate turnover
            turnover = sales_by_vehicle.merge(inv_by_vehicle, on="vehicle_id", how="left")
            turnover["avg_inventory"] = turnover["avg_inventory"].fillna(1)
            turnover["turnover_rate"] = turnover["total_sold"] / turnover["avg_inventory"]

            logger.info(f"Calculated inventory turnover for {len(turnover)} vehicles")
            return turnover

        except Exception as e:
            logger.error(f"Error calculating inventory turnover: {e}")
            raise

    @staticmethod
    def calculate_growth_rates(df: pd.DataFrame, value_column: str, period_column: str) -> pd.DataFrame:
        """Calculate period-over-period growth rates."""
        try:
            df_sorted = df.sort_values(period_column).copy()
            df_sorted["previous_value"] = df_sorted[value_column].shift(1)
            df_sorted["growth_rate"] = (
                (df_sorted[value_column] - df_sorted["previous_value"]) / df_sorted["previous_value"] * 100
            )

            logger.info(f"Calculated growth rates")
            return df_sorted

        except Exception as e:
            logger.error(f"Error calculating growth rates: {e}")
            raise

