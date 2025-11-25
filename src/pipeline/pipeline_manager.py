"""ETL Pipeline manager."""

from datetime import datetime, date, timedelta
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

from src.pipeline.extractors.data_extractor import DataExtractor
from src.pipeline.transformers.data_cleaner import DataCleaner
from src.pipeline.transformers.aggregator import DataAggregator
from src.pipeline.loaders.data_loader import DataLoader
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PipelineManager:
    """Orchestrate ETL pipeline workflows."""

    def __init__(self, db: Session):
        """Initialize pipeline manager."""
        self.db = db
        self.extractor = DataExtractor(db)
        self.cleaner = DataCleaner()
        self.aggregator = DataAggregator()
        self.loader = DataLoader(db)

    def run_sales_analytics_pipeline(
        self, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Run complete sales analytics pipeline."""
        try:
            logger.info("Starting sales analytics pipeline...")

            # Default to last 30 days if no dates provided
            if not end_date:
                end_date = datetime.now().date()
            if not start_date:
                start_date = end_date - timedelta(days=30)

            # Extract
            logger.info(f"Extracting sales data from {start_date} to {end_date}")
            sales_df = self.extractor.extract_sales_with_vehicle_info(start_date, end_date)

            if sales_df.empty:
                logger.warning("No sales data found for the specified period")
                return {"status": "no_data", "records": 0}

            # Clean
            sales_df = self.cleaner.remove_duplicates(sales_df)
            sales_df = self.cleaner.validate_positive_values(sales_df, ["total_amount", "quantity"])

            # Transform & Aggregate
            daily_sales = self.aggregator.aggregate_sales_by_period(sales_df, "D")
            sales_by_region = self.aggregator.aggregate_sales_by_region(sales_df)
            sales_by_category = self.aggregator.aggregate_sales_by_category(sales_df)
            sales_by_segment = self.aggregator.aggregate_sales_by_customer_segment(sales_df)
            top_vehicles = self.aggregator.aggregate_top_n_vehicles(sales_df, 10)

            # Load results
            self.loader.load_dataframe_to_analytics(daily_sales, "daily_sales")
            self.loader.load_dataframe_to_analytics(sales_by_region, "sales_by_region")
            self.loader.load_dataframe_to_analytics(sales_by_category, "sales_by_category")
            self.loader.load_dataframe_to_analytics(sales_by_segment, "sales_by_segment")
            self.loader.load_dataframe_to_analytics(top_vehicles, "top_vehicles")

            logger.info("Sales analytics pipeline completed successfully")

            return {
                "status": "success",
                "records_processed": len(sales_df),
                "start_date": str(start_date),
                "end_date": str(end_date),
                "snapshots_created": 5,
            }

        except Exception as e:
            logger.error(f"Error in sales analytics pipeline: {e}")
            raise

    def run_inventory_analytics_pipeline(self) -> Dict[str, Any]:
        """Run inventory analytics pipeline."""
        try:
            logger.info("Starting inventory analytics pipeline...")

            # Extract
            inventory_df = self.extractor.extract_inventory_with_vehicle_info()

            if inventory_df.empty:
                logger.warning("No inventory data found")
                return {"status": "no_data", "records": 0}

            # Clean
            inventory_df = self.cleaner.remove_duplicates(inventory_df)

            # Transform & Aggregate
            inventory_by_status = self.aggregator.aggregate_inventory_by_status(inventory_df)

            # Load results
            self.loader.load_dataframe_to_analytics(inventory_by_status, "inventory_by_status")

            # Calculate additional metrics
            total_inventory_value = (inventory_df["quantity_available"] * inventory_df["msrp"]).sum()
            low_stock_items = inventory_df[inventory_df["status"] == "low"]
            out_of_stock_items = inventory_df[inventory_df["status"] == "out_of_stock"]

            summary = {
                "total_inventory_value": float(total_inventory_value),
                "total_units": int(inventory_df["quantity_available"].sum()),
                "low_stock_count": len(low_stock_items),
                "out_of_stock_count": len(out_of_stock_items),
                "unique_vehicles": inventory_df["vehicle_id"].nunique(),
            }

            self.loader.load_analytics_snapshot("inventory_summary", summary)

            logger.info("Inventory analytics pipeline completed successfully")

            return {
                "status": "success",
                "records_processed": len(inventory_df),
                "snapshots_created": 2,
            }

        except Exception as e:
            logger.error(f"Error in inventory analytics pipeline: {e}")
            raise

    def run_full_pipeline(self, days_back: int = 30) -> Dict[str, Any]:
        """Run complete analytics pipeline."""
        try:
            logger.info("Starting full analytics pipeline...")

            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days_back)

            sales_result = self.run_sales_analytics_pipeline(start_date, end_date)
            inventory_result = self.run_inventory_analytics_pipeline()

            logger.info("Full pipeline completed successfully")

            return {
                "status": "success",
                "sales": sales_result,
                "inventory": inventory_result,
                "completed_at": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"Error in full pipeline: {e}")
            raise

