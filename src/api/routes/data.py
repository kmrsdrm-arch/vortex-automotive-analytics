"""Raw data access endpoints."""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel

from src.api.dependencies import get_db
from src.database.repositories.vehicle_repo import VehicleRepository
from src.database.repositories.sales_repo import SalesRepository
from src.database.repositories.inventory_repo import InventoryRepository
from src.data_generation.synthetic_data import SyntheticDataGenerator
from src.data_generation.seeder import DatabaseSeeder
from config.logging_config import logger

router = APIRouter(prefix="/api/v1/data", tags=["Data"])


class SeedRequest(BaseModel):
    """Request model for database seeding."""
    num_vehicles: int = 100
    num_sales: int = 10000
    months_back: int = 24


@router.get("/vehicles")
async def get_vehicles(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Max number of records to return"),
    category: Optional[str] = Query(None),
    make: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Get vehicle catalog."""
    repo = VehicleRepository(db)

    if category or make:
        vehicles = repo.search_vehicles(make=make, category=category)
    else:
        vehicles = repo.get_all(skip=skip, limit=limit)

    return [
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


@router.get("/vehicles/{vehicle_id}")
async def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    """Get specific vehicle details."""
    repo = VehicleRepository(db)
    vehicle = repo.get_by_id(vehicle_id)

    if not vehicle:
        return {"error": "Vehicle not found"}

    return {
        "id": vehicle.id,
        "vin": vehicle.vin,
        "make": vehicle.make,
        "model": vehicle.model,
        "year": vehicle.year,
        "category": vehicle.category,
        "trim": vehicle.trim,
        "msrp": float(vehicle.msrp),
        "specifications": vehicle.specifications,
    }


@router.get("/sales")
async def get_sales(
    skip: int = Query(0),
    limit: int = Query(100),
    region: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Get sales transactions."""
    repo = SalesRepository(db)

    if region:
        sales = repo.get_by_region(region)
    else:
        sales = repo.get_all(skip=skip, limit=limit)

    return [
        {
            "id": s.id,
            "vehicle_id": s.vehicle_id,
            "sale_date": s.sale_date.isoformat(),
            "quantity": s.quantity,
            "total_amount": float(s.total_amount),
            "customer_segment": s.customer_segment,
            "region": s.region,
        }
        for s in sales[:limit]
    ]


@router.get("/inventory")
async def get_inventory(
    skip: int = Query(0),
    limit: int = Query(100),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Get inventory records."""
    repo = InventoryRepository(db)

    if status:
        inventory = repo.get_by_status(status)
    else:
        inventory = repo.get_all(skip=skip, limit=limit)

    return [
        {
            "id": i.id,
            "vehicle_id": i.vehicle_id,
            "warehouse_location": i.warehouse_location,
            "region": i.region,
            "quantity_available": i.quantity_available,
            "status": i.status,
        }
        for i in inventory[:limit]
    ]


@router.post("/seed")
async def seed_database(
    seed_request: SeedRequest = SeedRequest(),
    db: Session = Depends(get_db)
):
    """
    Seed the database with synthetic data.
    
    This endpoint generates synthetic vehicles, sales transactions, and inventory records.
    Useful for testing and development purposes.
    
    Parameters:
    - num_vehicles: Number of vehicles to generate (default: 100)
    - num_sales: Number of sales transactions to generate (default: 10000)
    - months_back: How many months of historical data to generate (default: 24)
    """
    try:
        logger.info("Starting database seeding via API...")
        
        # Create generator and seeder
        generator = SyntheticDataGenerator(seed=42)
        seeder = DatabaseSeeder(db, generator)
        
        # Seed all data
        summary = seeder.seed_all(
            num_vehicles=seed_request.num_vehicles,
            num_sales=seed_request.num_sales,
            months_back=seed_request.months_back
        )
        
        logger.info("Database seeding completed successfully via API!")
        
        return {
            "success": True,
            "message": "Database seeded successfully",
            "summary": {
                "vehicles": summary['vehicles'],
                "inventory_records": summary['inventory'],
                "sales_transactions": summary['sales']
            }
        }
        
    except Exception as e:
        logger.error(f"Error seeding database via API: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to seed database: {str(e)}")

