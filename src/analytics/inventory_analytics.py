"""Inventory-specific analytics functions."""

import pandas as pd
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session

from src.pipeline.extractors.data_extractor import DataExtractor
from src.pipeline.transformers.aggregator import DataAggregator
from src.utils.logger import get_logger

logger = get_logger(__name__)


class InventoryAnalytics:
    """Inventory analytics calculator."""

    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db
        self.extractor = DataExtractor(db)
        self.aggregator = DataAggregator()

    def get_inventory_summary(self) -> Dict[str, Any]:
        """Get overall inventory summary."""
        try:
            df = self.extractor.extract_inventory_with_vehicle_info()

            if df.empty:
                return {
                    "total_units": 0,
                    "total_value": 0,
                    "unique_vehicles": 0,
                    "low_stock_count": 0,
                    "out_of_stock_count": 0,
                }

            summary = {
                "total_units": int(df["quantity_available"].sum()),
                "total_reserved": int(df["quantity_reserved"].sum()),
                "total_value": float((df["quantity_available"] * df["msrp"]).sum()),
                "unique_vehicles": int(df["vehicle_id"].nunique()),
                "low_stock_count": int((df["status"] == "low").sum()),
                "out_of_stock_count": int((df["status"] == "out_of_stock").sum()),
                "active_count": int((df["status"] == "active").sum()),
            }

            logger.info(f"Generated inventory summary: {summary['total_units']} units")
            return summary

        except Exception as e:
            logger.error(f"Error generating inventory summary: {e}")
            raise

    def get_inventory_by_region(self) -> List[Dict[str, Any]]:
        """Get inventory breakdown by region."""
        try:
            df = self.extractor.extract_inventory_with_vehicle_info()

            if df.empty:
                return []

            regional_df = (
                df.groupby("region")
                .agg(
                    {
                        "quantity_available": "sum",
                        "quantity_reserved": "sum",
                        "inventory_id": "count",
                    }
                )
                .rename(columns={"inventory_id": "record_count"})
                .reset_index()
            )

            regional = regional_df.to_dict(orient="records")

            logger.info(f"Generated inventory by region for {len(regional)} regions")
            return regional

        except Exception as e:
            logger.error(f"Error generating inventory by region: {e}")
            raise

    def get_inventory_by_category(self) -> List[Dict[str, Any]]:
        """Get inventory breakdown by vehicle category."""
        try:
            df = self.extractor.extract_inventory_with_vehicle_info()

            if df.empty:
                return []

            category_df = (
                df.groupby("category")
                .agg(
                    {
                        "quantity_available": "sum",
                        "quantity_reserved": "sum",
                        "inventory_id": "count",
                    }
                )
                .rename(columns={"inventory_id": "record_count"})
                .reset_index()
            )

            category = category_df.to_dict(orient="records")

            logger.info(f"Generated inventory by category for {len(category)} categories")
            return category

        except Exception as e:
            logger.error(f"Error generating inventory by category: {e}")
            raise

    def get_inventory_by_status(self) -> List[Dict[str, Any]]:
        """Get inventory breakdown by status."""
        try:
            df = self.extractor.extract_inventory_with_vehicle_info()

            if df.empty:
                return []

            status_df = self.aggregator.aggregate_inventory_by_status(df)
            # Rename for clarity in charts
            status_df = status_df.rename(columns={"quantity_available": "total_quantity"})
            
            status = status_df.to_dict(orient="records")

            logger.info(f"Generated inventory by status")
            return status

        except Exception as e:
            logger.error(f"Error generating inventory by status: {e}")
            raise

    def get_low_stock_alerts(self) -> List[Dict[str, Any]]:
        """Get vehicles with low stock levels."""
        try:
            df = self.extractor.extract_inventory_with_vehicle_info()

            if df.empty:
                return []

            low_stock_df = df[df["status"] == "low"][
                [
                    "vehicle_id",
                    "make",
                    "model",
                    "category",
                    "warehouse_location",
                    "region",
                    "quantity_available",
                ]
            ]

            alerts = low_stock_df.to_dict(orient="records")

            logger.info(f"Generated {len(alerts)} low stock alerts")
            return alerts

        except Exception as e:
            logger.error(f"Error generating low stock alerts: {e}")
            raise

    def get_overstock_items(self, threshold_multiplier: float = 3.0) -> List[Dict[str, Any]]:
        """Get vehicles that might be overstocked."""
        try:
            df = self.extractor.extract_inventory_with_vehicle_info()

            if df.empty:
                return []

            # Find items with quantity significantly above average for their category
            df_with_avg = df.merge(
                df.groupby("category")["quantity_available"]
                .mean()
                .rename("category_avg")
                .reset_index(),
                on="category",
            )

            overstock_df = df_with_avg[
                df_with_avg["quantity_available"] > df_with_avg["category_avg"] * threshold_multiplier
            ][["vehicle_id", "make", "model", "category", "warehouse_location", "quantity_available"]]

            overstock = overstock_df.to_dict(orient="records")

            logger.info(f"Found {len(overstock)} potential overstock items")
            return overstock

        except Exception as e:
            logger.error(f"Error finding overstock items: {e}")
            raise

    def get_warehouse_utilization(self) -> List[Dict[str, Any]]:
        """Get inventory utilization by warehouse."""
        try:
            df = self.extractor.extract_inventory_with_vehicle_info()

            if df.empty:
                return []

            warehouse_df = (
                df.groupby("warehouse_location")
                .agg(
                    {
                        "quantity_available": "sum",
                        "quantity_reserved": "sum",
                        "msrp": lambda x: (df.loc[x.index, "quantity_available"] * x).sum(),
                    }
                )
                .rename(columns={"msrp": "total_value"})
                .reset_index()
            )

            utilization = warehouse_df.to_dict(orient="records")

            logger.info(f"Generated warehouse utilization for {len(utilization)} warehouses")
            return utilization

        except Exception as e:
            logger.error(f"Error generating warehouse utilization: {e}")
            raise

