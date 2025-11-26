"""Raw data access endpoints."""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text, inspect
from typing import Optional
from pydantic import BaseModel

from src.api.dependencies import get_db
from src.database.repositories.vehicle_repo import VehicleRepository
from src.database.repositories.sales_repo import SalesRepository
from src.database.repositories.inventory_repo import InventoryRepository
from src.data_generation.synthetic_data import SyntheticDataGenerator
from src.data_generation.seeder import DatabaseSeeder
from config.logging_config import logger
from config.database import engine

# Import Base FIRST
from src.database.models.base import Base

# Then import ALL models to register them
from src.database.models.vehicle import Vehicle
from src.database.models.inventory import Inventory
from src.database.models.sales import Sales
from src.database.models.analytics import AnalyticsSnapshot, InsightHistory

router = APIRouter(prefix="/api/v1/data", tags=["Data"])


class SeedRequest(BaseModel):
    """Request model for database seeding."""
    num_vehicles: int = 100
    num_sales: int = 10000
    months_back: int = 24


@router.post("/reset-db")
async def reset_database():
    """
    Drop and recreate all database tables.
    
    WARNING: This will delete ALL data! Use with caution.
    """
    try:
        logger.info("Starting database reset - DROPPING ALL TABLES...")
        
        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        logger.info("All tables dropped successfully")
        
        # Create all tables fresh
        Base.metadata.create_all(bind=engine)
        logger.info("All tables recreated successfully")
        
        # Verify tables were created
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Tables after reset: {tables}")
        
        return {
            "success": True,
            "message": "Database reset successfully - all tables dropped and recreated",
            "tables": tables
        }
        
    except Exception as e:
        logger.error(f"Error resetting database: {e}")
        raise HTTPException(status_code=500, detail=f"Database reset failed: {str(e)}")


@router.post("/init-db")
async def initialize_database():
    """
    Initialize database schema by creating all tables.
    
    This endpoint should be called once after deployment to create
    the database schema. It's idempotent and safe to call multiple times.
    """
    try:
        logger.info("Starting manual database initialization...")
        
        # All models are already imported at module level
        # Check existing tables
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        logger.info(f"Existing tables before init: {existing_tables}")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Verify tables were created
        updated_tables = inspector.get_table_names()
        logger.info(f"Tables after init: {updated_tables}")
        
        # Expected tables
        expected = ['vehicles', 'inventory', 'sales', 'analytics_snapshots', 'insight_history']
        created = [t for t in expected if t in updated_tables and t not in existing_tables]
        already_exist = [t for t in expected if t in existing_tables]
        
        return {
            "success": True,
            "message": "Database initialized successfully",
            "tables_created": created,
            "tables_already_existed": already_exist,
            "all_tables": updated_tables
        }
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise HTTPException(status_code=500, detail=f"Database initialization failed: {str(e)}")


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
    
    Note: This operation may take 30-60 seconds for large datasets.
    """
    try:
        logger.info(f"Starting database seeding via API...")
        logger.info(f"Parameters: vehicles={seed_request.num_vehicles}, sales={seed_request.num_sales}, months_back={seed_request.months_back}")
        
        # Check database connection first
        try:
            db.execute(text("SELECT 1"))
            logger.info("✅ Database connection verified")
        except Exception as conn_err:
            logger.error(f"❌ Database connection failed: {conn_err}")
            raise HTTPException(
                status_code=503, 
                detail=f"Database connection failed. Please check if the database is accessible."
            )
        
        # Validate inputs
        if seed_request.num_vehicles < 1 or seed_request.num_vehicles > 1000:
            raise HTTPException(status_code=400, detail="num_vehicles must be between 1 and 1000")
        
        if seed_request.num_sales < 1 or seed_request.num_sales > 100000:
            raise HTTPException(status_code=400, detail="num_sales must be between 1 and 100000")
        
        if seed_request.months_back < 1 or seed_request.months_back > 60:
            raise HTTPException(status_code=400, detail="months_back must be between 1 and 60")
        
        # Create generator and seeder
        logger.info("Creating synthetic data generator...")
        generator = SyntheticDataGenerator(seed=42)
        
        logger.info("Creating database seeder...")
        seeder = DatabaseSeeder(db, generator)
        
        # Seed all data
        logger.info("Starting data generation and insertion...")
        summary = seeder.seed_all(
            num_vehicles=seed_request.num_vehicles,
            num_sales=seed_request.num_sales,
            months_back=seed_request.months_back
        )
        
        logger.info(f"✅ Database seeding completed successfully!")
        logger.info(f"Summary: {summary}")
        
        return {
            "success": True,
            "message": "Database seeded successfully",
            "summary": {
                "vehicles": summary['vehicles'],
                "inventory_records": summary['inventory'],
                "sales_transactions": summary['sales']
            },
            "note": "Data generation completed. You can now use the analytics endpoints."
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    
    except Exception as e:
        # Log full traceback for debugging
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"❌ Error seeding database via API: {e}")
        logger.error(f"Full traceback: {error_details}")
        
        raise HTTPException(
            status_code=500, 
            detail={
                "error": "Failed to seed database",
                "message": str(e),
                "hint": "Check server logs for detailed error information. Common issues: database tables not created, database connection lost, or insufficient memory."
            }
        )

