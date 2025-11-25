"""Seed database with synthetic data."""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import SessionLocal
from src.data_generation.synthetic_data import SyntheticDataGenerator
from src.data_generation.seeder import DatabaseSeeder
from config.logging_config import logger


def seed_database(num_vehicles: int = 100, num_sales: int = 10000, months_back: int = 24):
    """Seed database with synthetic data."""
    db = SessionLocal()

    try:
        logger.info("Starting database seeding process...")

        # Create generator and seeder
        generator = SyntheticDataGenerator(seed=42)
        seeder = DatabaseSeeder(db, generator)

        # Seed all data
        summary = seeder.seed_all(
            num_vehicles=num_vehicles, num_sales=num_sales, months_back=months_back
        )

        logger.info("=" * 50)
        logger.info("Database Seeding Summary:")
        logger.info(f"  Vehicles: {summary['vehicles']}")
        logger.info(f"  Inventory Records: {summary['inventory']}")
        logger.info(f"  Sales Transactions: {summary['sales']}")
        logger.info("=" * 50)
        logger.info("Database seeding completed successfully!")

    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Seed database with synthetic data")
    parser.add_argument(
        "--vehicles", type=int, default=100, help="Number of vehicles to generate"
    )
    parser.add_argument("--sales", type=int, default=10000, help="Number of sales to generate")
    parser.add_argument(
        "--months", type=int, default=24, help="Number of months of sales history"
    )

    args = parser.parse_args()

    seed_database(num_vehicles=args.vehicles, num_sales=args.sales, months_back=args.months)

