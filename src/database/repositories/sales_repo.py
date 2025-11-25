"""Sales repository with aggregation methods."""

from typing import List, Optional, Dict, Any
from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract
from src.database.models.sales import Sales
from src.database.models.vehicle import Vehicle
from src.database.repositories.base import BaseRepository
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SalesRepository(BaseRepository[Sales]):
    """Repository for Sales operations with aggregations."""

    def __init__(self, db: Session):
        super().__init__(Sales, db)

    def get_by_vehicle_id(self, vehicle_id: int) -> List[Sales]:
        """Get all sales for a specific vehicle."""
        try:
            return self.db.query(Sales).filter(Sales.vehicle_id == vehicle_id).all()
        except Exception as e:
            logger.error(f"Error fetching sales for vehicle {vehicle_id}: {e}")
            raise

    def get_by_date_range(self, start_date: date, end_date: date) -> List[Sales]:
        """Get sales within a date range."""
        try:
            return (
                self.db.query(Sales)
                .filter(Sales.sale_date >= start_date, Sales.sale_date <= end_date)
                .all()
            )
        except Exception as e:
            logger.error(f"Error fetching sales by date range: {e}")
            raise

    def get_by_region(self, region: str, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[Sales]:
        """Get sales for a specific region, optionally filtered by date."""
        try:
            query = self.db.query(Sales).filter(Sales.region == region)

            if start_date:
                query = query.filter(Sales.sale_date >= start_date)
            if end_date:
                query = query.filter(Sales.sale_date <= end_date)

            return query.all()
        except Exception as e:
            logger.error(f"Error fetching sales for region {region}: {e}")
            raise

    def get_by_customer_segment(self, segment: str) -> List[Sales]:
        """Get sales by customer segment."""
        try:
            return self.db.query(Sales).filter(Sales.customer_segment == segment).all()
        except Exception as e:
            logger.error(f"Error fetching sales for segment {segment}: {e}")
            raise

    def get_total_revenue(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> float:
        """Calculate total revenue, optionally filtered by date range."""
        try:
            query = self.db.query(func.sum(Sales.total_amount))

            if start_date:
                query = query.filter(Sales.sale_date >= start_date)
            if end_date:
                query = query.filter(Sales.sale_date <= end_date)

            result = query.scalar()
            return float(result) if result else 0.0
        except Exception as e:
            logger.error(f"Error calculating total revenue: {e}")
            raise

    def get_total_units_sold(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> int:
        """Calculate total units sold, optionally filtered by date range."""
        try:
            query = self.db.query(func.sum(Sales.quantity))

            if start_date:
                query = query.filter(Sales.sale_date >= start_date)
            if end_date:
                query = query.filter(Sales.sale_date <= end_date)

            result = query.scalar()
            return int(result) if result else 0
        except Exception as e:
            logger.error(f"Error calculating total units sold: {e}")
            raise

    def get_top_selling_vehicles(
        self, limit: int = 10, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Get top selling vehicles by quantity."""
        try:
            query = (
                self.db.query(
                    Sales.vehicle_id,
                    Vehicle.make,
                    Vehicle.model,
                    Vehicle.category,
                    func.sum(Sales.quantity).label("total_quantity"),
                    func.sum(Sales.total_amount).label("total_revenue"),
                )
                .join(Vehicle, Sales.vehicle_id == Vehicle.id)
            )

            if start_date:
                query = query.filter(Sales.sale_date >= start_date)
            if end_date:
                query = query.filter(Sales.sale_date <= end_date)

            results = (
                query.group_by(Sales.vehicle_id, Vehicle.make, Vehicle.model, Vehicle.category)
                .order_by(func.sum(Sales.quantity).desc())
                .limit(limit)
                .all()
            )

            return [
                {
                    "vehicle_id": r.vehicle_id,
                    "make": r.make,
                    "model": r.model,
                    "category": r.category,
                    "total_quantity": r.total_quantity,
                    "total_revenue": float(r.total_revenue),
                }
                for r in results
            ]
        except Exception as e:
            logger.error(f"Error fetching top selling vehicles: {e}")
            raise

    def get_sales_by_region(
        self, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Get sales aggregated by region."""
        try:
            query = self.db.query(
                Sales.region,
                func.sum(Sales.quantity).label("total_quantity"),
                func.sum(Sales.total_amount).label("total_revenue"),
                func.count(Sales.id).label("transaction_count"),
            )

            if start_date:
                query = query.filter(Sales.sale_date >= start_date)
            if end_date:
                query = query.filter(Sales.sale_date <= end_date)

            results = query.group_by(Sales.region).all()

            return [
                {
                    "region": r.region,
                    "total_quantity": r.total_quantity,
                    "total_revenue": float(r.total_revenue),
                    "transaction_count": r.transaction_count,
                }
                for r in results
            ]
        except Exception as e:
            logger.error(f"Error fetching sales by region: {e}")
            raise

    def get_sales_by_customer_segment(
        self, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Get sales aggregated by customer segment."""
        try:
            query = self.db.query(
                Sales.customer_segment,
                func.sum(Sales.quantity).label("total_quantity"),
                func.sum(Sales.total_amount).label("total_revenue"),
            )

            if start_date:
                query = query.filter(Sales.sale_date >= start_date)
            if end_date:
                query = query.filter(Sales.sale_date <= end_date)

            results = query.group_by(Sales.customer_segment).all()

            return [
                {
                    "customer_segment": r.customer_segment,
                    "total_quantity": r.total_quantity,
                    "total_revenue": float(r.total_revenue),
                }
                for r in results
            ]
        except Exception as e:
            logger.error(f"Error fetching sales by customer segment: {e}")
            raise

    def get_monthly_sales_trend(self, year: int) -> List[Dict[str, Any]]:
        """Get monthly sales trend for a specific year."""
        try:
            results = (
                self.db.query(
                    extract("month", Sales.sale_date).label("month"),
                    func.sum(Sales.quantity).label("total_quantity"),
                    func.sum(Sales.total_amount).label("total_revenue"),
                )
                .filter(extract("year", Sales.sale_date) == year)
                .group_by(extract("month", Sales.sale_date))
                .order_by(extract("month", Sales.sale_date))
                .all()
            )

            return [
                {
                    "month": int(r.month),
                    "total_quantity": r.total_quantity,
                    "total_revenue": float(r.total_revenue),
                }
                for r in results
            ]
        except Exception as e:
            logger.error(f"Error fetching monthly sales trend for year {year}: {e}")
            raise

