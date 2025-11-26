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


@router.post("/diagnose-db")
async def diagnose_database():
    """
    Comprehensive database diagnostics using raw SQL and SQLAlchemy.
    
    This endpoint performs multiple tests to identify why tables aren't being created:
    1. Basic connectivity test
    2. User/database information
    3. Schema verification
    4. Permission checks
    5. Raw SQL table creation test
    6. SQLAlchemy metadata inspection
    7. SQLAlchemy create_all test
    """
    results = {
        "tests": {},
        "summary": "",
        "recommendations": []
    }
    
    try:
        # Test 1: Basic connectivity
        logger.info("TEST 1: Basic connectivity check")
        try:
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1 as test")).fetchone()
                results["tests"]["connectivity"] = {
                    "status": "PASS",
                    "result": f"Database responded: {result[0]}"
                }
                logger.info("✓ Connectivity test PASSED")
        except Exception as e:
            results["tests"]["connectivity"] = {
                "status": "FAIL",
                "error": str(e)
            }
            logger.error(f"✗ Connectivity test FAILED: {e}")
            
        # Test 2: User and database information
        logger.info("TEST 2: User and database information")
        try:
            with engine.connect() as conn:
                result = conn.execute(text(
                    "SELECT current_user, current_database(), current_schema()"
                )).fetchone()
                results["tests"]["user_info"] = {
                    "status": "PASS",
                    "current_user": result[0],
                    "current_database": result[1],
                    "current_schema": result[2]
                }
                logger.info(f"✓ Connected as user: {result[0]}, database: {result[1]}, schema: {result[2]}")
        except Exception as e:
            results["tests"]["user_info"] = {
                "status": "FAIL",
                "error": str(e)
            }
            logger.error(f"✗ User info test FAILED: {e}")
            
        # Test 3: List existing tables with raw SQL
        logger.info("TEST 3: List existing tables (raw SQL)")
        try:
            with engine.connect() as conn:
                result = conn.execute(text(
                    "SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename"
                )).fetchall()
                tables = [row[0] for row in result]
                results["tests"]["existing_tables_raw"] = {
                    "status": "PASS",
                    "tables": tables,
                    "count": len(tables)
                }
                logger.info(f"✓ Found {len(tables)} tables via raw SQL: {tables}")
        except Exception as e:
            results["tests"]["existing_tables_raw"] = {
                "status": "FAIL",
                "error": str(e)
            }
            logger.error(f"✗ List tables test FAILED: {e}")
            
        # Test 4: Check table creation permissions
        logger.info("TEST 4: Check CREATE TABLE permissions")
        try:
            with engine.connect() as conn:
                # Try to create a test table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS diagnostic_test (
                        id SERIAL PRIMARY KEY,
                        test_col VARCHAR(50),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                conn.commit()
                
                # Verify it was created
                result = conn.execute(text(
                    "SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname='public' AND tablename='diagnostic_test')"
                )).fetchone()
                
                table_exists = result[0]
                
                # Clean up
                if table_exists:
                    conn.execute(text("DROP TABLE diagnostic_test"))
                    conn.commit()
                
                results["tests"]["create_permission"] = {
                    "status": "PASS" if table_exists else "FAIL",
                    "can_create_tables": table_exists,
                    "message": "Successfully created and dropped test table" if table_exists else "Failed to create test table"
                }
                logger.info(f"✓ CREATE permission test: {'PASSED' if table_exists else 'FAILED'}")
        except Exception as e:
            results["tests"]["create_permission"] = {
                "status": "FAIL",
                "error": str(e)
            }
            logger.error(f"✗ CREATE permission test FAILED: {e}")
            
        # Test 5: Check what SQLAlchemy metadata knows
        logger.info("TEST 5: SQLAlchemy metadata inspection")
        try:
            registered_tables = list(Base.metadata.tables.keys())
            results["tests"]["sqlalchemy_metadata"] = {
                "status": "PASS",
                "registered_tables": registered_tables,
                "count": len(registered_tables),
                "expected": ['vehicles', 'inventory', 'sales', 'analytics_snapshots', 'insight_history']
            }
            logger.info(f"✓ Base.metadata knows about {len(registered_tables)} tables: {registered_tables}")
            
            if len(registered_tables) == 0:
                results["recommendations"].append("CRITICAL: No tables registered in Base.metadata - models may not be imported correctly")
            elif len(registered_tables) < 5:
                results["recommendations"].append(f"WARNING: Only {len(registered_tables)} tables registered, expected 5")
        except Exception as e:
            results["tests"]["sqlalchemy_metadata"] = {
                "status": "FAIL",
                "error": str(e)
            }
            logger.error(f"✗ Metadata inspection FAILED: {e}")
            
        # Test 6: Try SQLAlchemy create_all
        logger.info("TEST 6: SQLAlchemy create_all test")
        try:
            # Dispose connections first
            engine.dispose()
            logger.info("Disposed all connections before create_all")
            
            # Get tables before
            inspector = inspect(engine)
            before_tables = inspector.get_table_names()
            logger.info(f"Tables before create_all: {before_tables}")
            
            # Create all tables
            Base.metadata.create_all(bind=engine)
            logger.info("create_all() executed")
            
            # Dispose connections after
            engine.dispose()
            logger.info("Disposed all connections after create_all")
            
            # Get tables after with fresh connection
            inspector = inspect(engine)
            after_tables = inspector.get_table_names()
            logger.info(f"Tables after create_all: {after_tables}")
            
            new_tables = [t for t in after_tables if t not in before_tables]
            
            results["tests"]["sqlalchemy_create_all"] = {
                "status": "PASS" if len(new_tables) > 0 or len(after_tables) >= 5 else "PARTIAL",
                "before": before_tables,
                "after": after_tables,
                "new_tables": new_tables
            }
            logger.info(f"✓ create_all test completed. New tables: {new_tables}")
            
            if len(after_tables) == 0:
                results["recommendations"].append("CRITICAL: create_all() executed but no tables exist - possible permission or schema issue")
            elif len(new_tables) == 0 and len(after_tables) >= 5:
                results["recommendations"].append("INFO: Tables already exist, create_all() is idempotent")
        except Exception as e:
            results["tests"]["sqlalchemy_create_all"] = {
                "status": "FAIL",
                "error": str(e)
            }
            logger.error(f"✗ create_all test FAILED: {e}")
            results["recommendations"].append(f"ERROR during create_all: {str(e)}")
            
        # Test 7: Try creating one table with raw DDL
        logger.info("TEST 7: Raw DDL table creation test")
        try:
            with engine.connect() as conn:
                # Create a simple version of the vehicles table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS vehicles_test (
                        id SERIAL PRIMARY KEY,
                        vin VARCHAR(17) UNIQUE NOT NULL,
                        make VARCHAR(50) NOT NULL,
                        model VARCHAR(100) NOT NULL,
                        year INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                conn.commit()
                
                # Check if it was created
                result = conn.execute(text(
                    "SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname='public' AND tablename='vehicles_test')"
                )).fetchone()
                
                table_exists = result[0]
                
                # Clean up
                if table_exists:
                    conn.execute(text("DROP TABLE vehicles_test"))
                    conn.commit()
                
                results["tests"]["raw_ddl"] = {
                    "status": "PASS" if table_exists else "FAIL",
                    "can_create_with_ddl": table_exists,
                    "message": "Raw DDL successfully created table" if table_exists else "Raw DDL failed to create table"
                }
                logger.info(f"✓ Raw DDL test: {'PASSED' if table_exists else 'FAILED'}")
                
                if table_exists and len(Base.metadata.tables) == 0:
                    results["recommendations"].append("CRITICAL: Raw SQL works but SQLAlchemy metadata is empty - model imports may be broken")
                elif not table_exists:
                    results["recommendations"].append("CRITICAL: Cannot create tables even with raw SQL - check database permissions")
        except Exception as e:
            results["tests"]["raw_ddl"] = {
                "status": "FAIL",
                "error": str(e)
            }
            logger.error(f"✗ Raw DDL test FAILED: {e}")
            
        # Generate summary
        passed = sum(1 for t in results["tests"].values() if t["status"] == "PASS")
        total = len(results["tests"])
        results["summary"] = f"Passed {passed}/{total} tests"
        
        logger.info(f"DIAGNOSTIC COMPLETE: {results['summary']}")
        logger.info(f"Recommendations: {results['recommendations']}")
        
        return results
        
    except Exception as e:
        logger.error(f"Diagnostic endpoint failed: {e}")
        raise HTTPException(status_code=500, detail=f"Diagnostic failed: {str(e)}")


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
        
        # Dispose all connections to ensure clean state
        engine.dispose()
        logger.info("Disposed all database connections")
        
        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        logger.info("All tables dropped successfully")
        
        # Create all tables fresh
        Base.metadata.create_all(bind=engine)
        logger.info("All tables recreated successfully")
        
        # Dispose connections again to force reconnection
        engine.dispose()
        logger.info("Disposed connections to force fresh connections")
        
        # Verify tables were created with a fresh connection
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
        # Check what tables Base.metadata knows about
        logger.info(f"Tables registered in Base.metadata: {list(Base.metadata.tables.keys())}")
        
        # Check existing tables
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        logger.info(f"Existing tables before init: {existing_tables}")
        
        # Dispose connections before creating to ensure clean state
        engine.dispose()
        logger.info("Disposed all database connections before create_all")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("create_all() completed")
        
        # Dispose connections after creating to force fresh connections
        engine.dispose()
        logger.info("Disposed all database connections after create_all")
        
        # Verify tables were created with fresh connection
        inspector = inspect(engine)
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

