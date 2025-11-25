"""Vehicle repository with custom queries."""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.database.models.vehicle import Vehicle
from src.database.repositories.base import BaseRepository
from src.utils.logger import get_logger

logger = get_logger(__name__)


class VehicleRepository(BaseRepository[Vehicle]):
    """Repository for Vehicle operations."""

    def __init__(self, db: Session):
        super().__init__(Vehicle, db)

    def get_by_vin(self, vin: str) -> Optional[Vehicle]:
        """Get vehicle by VIN."""
        try:
            return self.db.query(Vehicle).filter(Vehicle.vin == vin).first()
        except Exception as e:
            logger.error(f"Error fetching vehicle by VIN {vin}: {e}")
            raise

    def get_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """Get vehicles by category."""
        try:
            return (
                self.db.query(Vehicle)
                .filter(Vehicle.category == category)
                .offset(skip)
                .limit(limit)
                .all()
            )
        except Exception as e:
            logger.error(f"Error fetching vehicles by category {category}: {e}")
            raise

    def get_by_make_model(self, make: str, model: str) -> List[Vehicle]:
        """Get vehicles by make and model."""
        try:
            return (
                self.db.query(Vehicle).filter(Vehicle.make == make, Vehicle.model == model).all()
            )
        except Exception as e:
            logger.error(f"Error fetching vehicles by make {make} and model {model}: {e}")
            raise

    def get_by_year_range(self, start_year: int, end_year: int) -> List[Vehicle]:
        """Get vehicles within a year range."""
        try:
            return (
                self.db.query(Vehicle)
                .filter(Vehicle.year >= start_year, Vehicle.year <= end_year)
                .all()
            )
        except Exception as e:
            logger.error(f"Error fetching vehicles by year range {start_year}-{end_year}: {e}")
            raise

    def search_vehicles(
        self,
        make: Optional[str] = None,
        model: Optional[str] = None,
        category: Optional[str] = None,
        year: Optional[int] = None,
    ) -> List[Vehicle]:
        """Search vehicles with multiple filters."""
        try:
            query = self.db.query(Vehicle)

            if make:
                query = query.filter(Vehicle.make.ilike(f"%{make}%"))
            if model:
                query = query.filter(Vehicle.model.ilike(f"%{model}%"))
            if category:
                query = query.filter(Vehicle.category == category)
            if year:
                query = query.filter(Vehicle.year == year)

            return query.all()
        except Exception as e:
            logger.error(f"Error searching vehicles: {e}")
            raise

    def get_unique_makes(self) -> List[str]:
        """Get list of unique vehicle makes."""
        try:
            return [make[0] for make in self.db.query(Vehicle.make).distinct().all()]
        except Exception as e:
            logger.error(f"Error fetching unique makes: {e}")
            raise

    def get_unique_categories(self) -> List[str]:
        """Get list of unique categories."""
        try:
            return [cat[0] for cat in self.db.query(Vehicle.category).distinct().all()]
        except Exception as e:
            logger.error(f"Error fetching unique categories: {e}")
            raise

