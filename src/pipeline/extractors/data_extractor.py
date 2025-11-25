"""Data extraction from database."""

from typing import List, Optional, Dict, Any
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
import pandas as pd

from src.database.models import Vehicle, Inventory, Sales
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DataExtractor:
    """Extract data from database for processing."""

    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db

    def extract_vehicles(self, filters: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """Extract vehicle data."""
        try:
            query = self.db.query(Vehicle)

            if filters:
                if "category" in filters:
                    query = query.filter(Vehicle.category == filters["category"])
                if "make" in filters:
                    query = query.filter(Vehicle.make == filters["make"])
                if "year" in filters:
                    query = query.filter(Vehicle.year == filters["year"])

            vehicles = query.all()

            data = [
                {
                    "id": v.id,
                    "vin": v.vin,
                    "make": v.make,
                    "model": v.model,
                    "year": v.year,
                    "category": v.category,
                    "trim": v.trim,
                    "msrp": float(v.msrp),
                }
                for v in vehicles
            ]

            df = pd.DataFrame(data)
            logger.info(f"Extracted {len(df)} vehicles")
            return df

        except Exception as e:
            logger.error(f"Error extracting vehicles: {e}")
            raise

    def extract_inventory(self, filters: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """Extract inventory data."""
        try:
            query = self.db.query(Inventory)

            if filters:
                if "region" in filters:
                    query = query.filter(Inventory.region == filters["region"])
                if "status" in filters:
                    query = query.filter(Inventory.status == filters["status"])
                if "warehouse" in filters:
                    query = query.filter(Inventory.warehouse_location == filters["warehouse"])

            inventory = query.all()

            data = [
                {
                    "id": i.id,
                    "vehicle_id": i.vehicle_id,
                    "warehouse_location": i.warehouse_location,
                    "region": i.region,
                    "quantity_available": i.quantity_available,
                    "quantity_reserved": i.quantity_reserved,
                    "reorder_point": i.reorder_point,
                    "status": i.status,
                    "last_restocked": i.last_restocked,
                }
                for i in inventory
            ]

            df = pd.DataFrame(data)
            logger.info(f"Extracted {len(df)} inventory records")
            return df

        except Exception as e:
            logger.error(f"Error extracting inventory: {e}")
            raise

    def extract_sales(
        self, start_date: Optional[date] = None, end_date: Optional[date] = None, filters: Optional[Dict[str, Any]] = None
    ) -> pd.DataFrame:
        """Extract sales data."""
        try:
            query = self.db.query(Sales)

            # Date range filters
            if start_date:
                query = query.filter(Sales.sale_date >= start_date)
            if end_date:
                query = query.filter(Sales.sale_date <= end_date)

            # Additional filters
            if filters:
                if "region" in filters:
                    query = query.filter(Sales.region == filters["region"])
                if "customer_segment" in filters:
                    query = query.filter(Sales.customer_segment == filters["customer_segment"])
                if "vehicle_id" in filters:
                    query = query.filter(Sales.vehicle_id == filters["vehicle_id"])

            sales = query.all()

            data = [
                {
                    "id": s.id,
                    "vehicle_id": s.vehicle_id,
                    "sale_date": s.sale_date,
                    "quantity": s.quantity,
                    "unit_price": float(s.unit_price),
                    "total_amount": float(s.total_amount),
                    "customer_segment": s.customer_segment,
                    "region": s.region,
                    "salesperson_id": s.salesperson_id,
                    "discount_applied": float(s.discount_applied),
                }
                for s in sales
            ]

            df = pd.DataFrame(data)
            logger.info(f"Extracted {len(df)} sales records")
            return df

        except Exception as e:
            logger.error(f"Error extracting sales: {e}")
            raise

    def extract_sales_with_vehicle_info(
        self, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> pd.DataFrame:
        """Extract sales data joined with vehicle information."""
        try:
            query = self.db.query(Sales, Vehicle).join(Vehicle, Sales.vehicle_id == Vehicle.id)

            if start_date:
                query = query.filter(Sales.sale_date >= start_date)
            if end_date:
                query = query.filter(Sales.sale_date <= end_date)

            results = query.all()

            data = [
                {
                    "sale_id": s.id,
                    "vehicle_id": s.vehicle_id,
                    "sale_date": s.sale_date,
                    "quantity": s.quantity,
                    "unit_price": float(s.unit_price),
                    "total_amount": float(s.total_amount),
                    "customer_segment": s.customer_segment,
                    "region": s.region,
                    "discount_applied": float(s.discount_applied),
                    "make": v.make,
                    "model": v.model,
                    "year": v.year,
                    "category": v.category,
                    "msrp": float(v.msrp),
                }
                for s, v in results
            ]

            df = pd.DataFrame(data)
            logger.info(f"Extracted {len(df)} sales records with vehicle info")
            return df

        except Exception as e:
            logger.error(f"Error extracting sales with vehicle info: {e}")
            raise

    def extract_inventory_with_vehicle_info(self) -> pd.DataFrame:
        """Extract inventory data joined with vehicle information."""
        try:
            results = (
                self.db.query(Inventory, Vehicle)
                .join(Vehicle, Inventory.vehicle_id == Vehicle.id)
                .all()
            )

            data = [
                {
                    "inventory_id": i.id,
                    "vehicle_id": i.vehicle_id,
                    "warehouse_location": i.warehouse_location,
                    "region": i.region,
                    "quantity_available": i.quantity_available,
                    "quantity_reserved": i.quantity_reserved,
                    "status": i.status,
                    "make": v.make,
                    "model": v.model,
                    "year": v.year,
                    "category": v.category,
                    "msrp": float(v.msrp),
                }
                for i, v in results
            ]

            df = pd.DataFrame(data)
            logger.info(f"Extracted {len(df)} inventory records with vehicle info")
            return df

        except Exception as e:
            logger.error(f"Error extracting inventory with vehicle info: {e}")
            raise

