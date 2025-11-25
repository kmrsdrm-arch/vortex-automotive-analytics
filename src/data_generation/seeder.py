"""Database seeder script."""

from typing import List, Dict
from sqlalchemy.orm import Session
from src.data_generation.synthetic_data import SyntheticDataGenerator
from src.database.models import Vehicle, Inventory, Sales
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DatabaseSeeder:
    """Seed database with synthetic data."""

    def __init__(self, db: Session, generator: SyntheticDataGenerator):
        """Initialize seeder with database session and generator."""
        self.db = db
        self.generator = generator

    def seed_vehicles(self, count: int = 100) -> List[int]:
        """Seed vehicles and return their IDs."""
        logger.info(f"Seeding {count} vehicles...")

        vehicle_data = self.generator.generate_vehicles(count)
        vehicle_ids = []

        for veh_data in vehicle_data:
            vehicle = Vehicle(**veh_data)
            self.db.add(vehicle)
            self.db.flush()  # Flush to get the ID
            vehicle_ids.append(vehicle.id)

        self.db.commit()
        logger.info(f"Seeded {len(vehicle_ids)} vehicles")
        return vehicle_ids

    def seed_inventory(self, vehicle_ids: List[int]) -> int:
        """Seed inventory records."""
        logger.info(f"Seeding inventory for {len(vehicle_ids)} vehicles...")

        inventory_data = self.generator.generate_inventory(vehicle_ids)

        for inv_data in inventory_data:
            inventory = Inventory(**inv_data)
            self.db.add(inventory)

        self.db.commit()
        logger.info(f"Seeded {len(inventory_data)} inventory records")
        return len(inventory_data)

    def seed_sales(
        self, vehicle_data: List[Dict], num_sales: int = 10000, months_back: int = 24
    ) -> int:
        """Seed sales records."""
        logger.info(f"Seeding {num_sales} sales records...")

        sales_data = self.generator.generate_sales(vehicle_data, num_sales, months_back)

        # Batch insert for performance
        batch_size = 1000
        for i in range(0, len(sales_data), batch_size):
            batch = sales_data[i : i + batch_size]
            for sale_data in batch:
                sale = Sales(**sale_data)
                self.db.add(sale)
            self.db.commit()
            logger.info(f"Seeded batch {i // batch_size + 1}")

        logger.info(f"Seeded {len(sales_data)} sales records")
        return len(sales_data)

    def seed_all(
        self,
        num_vehicles: int = 100,
        num_sales: int = 10000,
        months_back: int = 24,
    ) -> Dict[str, int]:
        """Seed all data."""
        logger.info("Starting database seeding...")

        try:
            # Clear existing data (optional - be careful in production!)
            logger.info("Clearing existing data...")
            self.db.query(Sales).delete()
            self.db.query(Inventory).delete()
            self.db.query(Vehicle).delete()
            self.db.commit()

            # Seed vehicles
            vehicle_ids = self.seed_vehicles(num_vehicles)

            # Get vehicle data for sales generation
            vehicles = self.db.query(Vehicle).all()
            vehicle_data = [
                {
                    "vin": v.vin,
                    "make": v.make,
                    "model": v.model,
                    "year": v.year,
                    "category": v.category,
                    "msrp": v.msrp,
                }
                for v in vehicles
            ]

            # Seed inventory
            inventory_count = self.seed_inventory(vehicle_ids)

            # Seed sales
            sales_count = self.seed_sales(vehicle_data, num_sales, months_back)

            summary = {
                "vehicles": len(vehicle_ids),
                "inventory": inventory_count,
                "sales": sales_count,
            }

            logger.info(f"Database seeding completed: {summary}")
            return summary

        except Exception as e:
            logger.error(f"Error during database seeding: {e}")
            self.db.rollback()
            raise


# For type hints
from typing import List, Dict

