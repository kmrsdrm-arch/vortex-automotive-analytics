"""Synthetic data generator for automotive sales and inventory."""

import random
from datetime import datetime, timedelta, date
from typing import List, Dict, Any
from faker import Faker
from decimal import Decimal

from src.data_generation.schemas import (
    AUTOMOTIVE_CATALOG,
    TRIM_LEVELS,
    WAREHOUSE_LOCATIONS,
    REGIONS,
    CUSTOMER_SEGMENTS,
    SEGMENT_WEIGHTS,
    SEASONAL_FACTORS,
    REGIONAL_PREFERENCES,
    get_category_for_model,
    get_msrp_range,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)
fake = Faker()


class SyntheticDataGenerator:
    """Generate realistic synthetic automotive data."""

    def __init__(self, seed: int = 42):
        """Initialize generator with a seed for reproducibility."""
        self.seed = seed
        random.seed(seed)
        Faker.seed(seed)
        logger.info(f"Initialized SyntheticDataGenerator with seed {seed}")

    def generate_vin(self) -> str:
        """Generate a realistic-looking VIN (17 characters)."""
        chars = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"
        return "".join(random.choices(chars, k=17))

    def generate_vehicles(self, count: int = 100) -> List[Dict[str, Any]]:
        """Generate vehicle catalog data."""
        logger.info(f"Generating {count} vehicles...")
        vehicles = []
        years = list(range(2020, 2025))

        for _ in range(count):
            make = random.choice(list(AUTOMOTIVE_CATALOG.keys()))
            model = random.choice(AUTOMOTIVE_CATALOG[make])
            year = random.choice(years)
            category = get_category_for_model(model)
            trim = random.choice(TRIM_LEVELS)

            # Generate MSRP based on category
            msrp_min, msrp_max = get_msrp_range(category)
            msrp = round(random.uniform(msrp_min, msrp_max), 2)

            # Generate specifications
            specifications = {
                "engine": random.choice(
                    ["2.0L I4", "2.5L I4", "3.5L V6", "5.0L V8", "Hybrid", "Electric"]
                ),
                "transmission": random.choice(["Automatic", "Manual", "CVT"]),
                "drivetrain": random.choice(["FWD", "RWD", "AWD", "4WD"]),
                "fuel_economy_city": random.randint(18, 35),
                "fuel_economy_highway": random.randint(24, 45),
                "horsepower": random.randint(150, 450),
                "color": random.choice(
                    ["White", "Black", "Silver", "Gray", "Red", "Blue", "Green"]
                ),
            }

            vehicle = {
                "vin": self.generate_vin(),
                "make": make,
                "model": model,
                "year": year,
                "category": category,
                "trim": trim,
                "msrp": Decimal(str(msrp)),
                "specifications": specifications,
            }
            vehicles.append(vehicle)

        logger.info(f"Generated {len(vehicles)} vehicles")
        return vehicles

    def generate_inventory(self, vehicle_ids: List[int]) -> List[Dict[str, Any]]:
        """Generate inventory records for vehicles across warehouses."""
        logger.info(f"Generating inventory for {len(vehicle_ids)} vehicles...")
        inventory_records = []

        for vehicle_id in vehicle_ids:
            # Not all vehicles need to be in all warehouses
            num_warehouses = random.randint(2, 6)
            selected_warehouses = random.sample(WAREHOUSE_LOCATIONS, num_warehouses)

            for warehouse in selected_warehouses:
                # Generate realistic quantities
                quantity_available = random.randint(5, 50)
                quantity_reserved = random.randint(0, min(5, quantity_available // 2))
                reorder_point = random.randint(5, 15)

                # Determine status
                if quantity_available == 0:
                    status = "out_of_stock"
                elif quantity_available < reorder_point:
                    status = "low"
                else:
                    status = "active"

                # Last restocked within the last 90 days
                days_ago = random.randint(1, 90)
                last_restocked = datetime.now() - timedelta(days=days_ago)

                inventory = {
                    "vehicle_id": vehicle_id,
                    "warehouse_location": warehouse["location"],
                    "region": warehouse["region"],
                    "quantity_available": quantity_available,
                    "quantity_reserved": quantity_reserved,
                    "reorder_point": reorder_point,
                    "last_restocked": last_restocked,
                    "status": status,
                }
                inventory_records.append(inventory)

        logger.info(f"Generated {len(inventory_records)} inventory records")
        return inventory_records

    def generate_sales(
        self,
        vehicle_data: List[Dict[str, Any]],
        num_sales: int = 10000,
        months_back: int = 24,
    ) -> List[Dict[str, Any]]:
        """Generate sales transactions with realistic patterns."""
        logger.info(f"Generating {num_sales} sales transactions...")
        sales_records = []

        # Create a mapping of vehicles with their categories and MSRPs
        vehicles_by_category = {}
        vehicle_lookup = {}

        for idx, vehicle in enumerate(vehicle_data, start=1):
            category = vehicle["category"]
            if category not in vehicles_by_category:
                vehicles_by_category[category] = []
            vehicles_by_category[category].append(idx)
            vehicle_lookup[idx] = vehicle

        # Generate sales over the time period
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30 * months_back)

        for _ in range(num_sales):
            # Random date within range
            days_offset = random.randint(0, (end_date - start_date).days)
            sale_date = start_date + timedelta(days=days_offset)

            # Apply seasonal factor
            month = sale_date.month
            seasonal_factor = SEASONAL_FACTORS.get(month, 1.0)

            # Select region (with some randomness)
            region = random.choice(REGIONS)

            # Select category based on regional preferences
            category_prefs = REGIONAL_PREFERENCES.get(region, {})
            if category_prefs and random.random() < 0.8:  # 80% follow regional preferences
                categories = list(category_prefs.keys())
                weights = list(category_prefs.values())
                category = random.choices(categories, weights=weights)[0]
            else:
                category = random.choice(list(vehicles_by_category.keys()))

            # Select vehicle from category
            if category in vehicles_by_category and vehicles_by_category[category]:
                vehicle_id = random.choice(vehicles_by_category[category])
            else:
                vehicle_id = random.randint(1, len(vehicle_data))

            vehicle = vehicle_lookup.get(vehicle_id, vehicle_data[0])

            # Customer segment
            customer_segment = random.choices(CUSTOMER_SEGMENTS, weights=SEGMENT_WEIGHTS)[0]

            # Quantity (fleet and dealer buy more)
            if customer_segment == "individual":
                quantity = 1
            elif customer_segment == "fleet":
                quantity = random.randint(3, 20)
            else:  # dealer
                quantity = random.randint(5, 30)

            # Pricing with discounts
            base_price = float(vehicle["msrp"])
            discount_pct = 0

            # Apply discounts based on segment and season
            if customer_segment == "fleet":
                discount_pct = random.uniform(5, 15)
            elif customer_segment == "dealer":
                discount_pct = random.uniform(10, 20)
            else:
                discount_pct = random.uniform(0, 8)

            # Additional discount in slow months
            if seasonal_factor < 1.0:
                discount_pct += random.uniform(0, 5)

            discount_pct = min(discount_pct, 25)  # Cap at 25%

            unit_price = base_price * (1 - discount_pct / 100)
            total_amount = unit_price * quantity

            # Salesperson ID
            salesperson_id = f"SP{random.randint(1000, 9999)}"

            sale = {
                "vehicle_id": vehicle_id,
                "sale_date": sale_date,
                "quantity": quantity,
                "unit_price": Decimal(str(round(unit_price, 2))),
                "total_amount": Decimal(str(round(total_amount, 2))),
                "customer_segment": customer_segment,
                "region": region,
                "salesperson_id": salesperson_id,
                "discount_applied": Decimal(str(round(discount_pct, 2))),
            }
            sales_records.append(sale)

        # Sort by date
        sales_records.sort(key=lambda x: x["sale_date"])

        logger.info(f"Generated {len(sales_records)} sales records")
        return sales_records

