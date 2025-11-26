"""
Production Database Initialization Script
==========================================

This script initializes the database schema for production deployment.
Run this once after deploying to create all necessary tables.

Usage:
    python init_production_db.py
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import text, inspect
from config.database import engine
from src.utils.logger import get_logger

# Import all models FIRST to register them with Base.metadata
from src.database.models.vehicle import Vehicle
from src.database.models.inventory import Inventory
from src.database.models.sales import Sales
from src.database.models.analytics import AnalyticsSnapshot, InsightHistory
from src.database.models import Base

logger = get_logger(__name__)


def check_database_connection():
    """Check if database is accessible."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✅ Database connection successful")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False


def check_existing_tables():
    """Check what tables already exist."""
    try:
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        
        if existing_tables:
            logger.info(f"📋 Existing tables: {', '.join(existing_tables)}")
        else:
            logger.info("📋 No existing tables found")
        
        return existing_tables
    except Exception as e:
        logger.error(f"❌ Error checking tables: {e}")
        return []


def create_tables():
    """Create all database tables."""
    try:
        logger.info("🏗️  Creating database tables...")
        
        # All models are already imported at module level
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        logger.info("✅ Database tables created successfully")
        
        # Verify tables were created
        inspector = inspect(engine)
        created_tables = inspector.get_table_names()
        logger.info(f"📊 Tables in database: {', '.join(created_tables)}")
        
        # Expected tables
        expected = ['vehicles', 'inventory', 'sales', 'analytics_snapshots', 'insight_history']
        missing = [t for t in expected if t not in created_tables]
        
        if missing:
            logger.warning(f"⚠️  Missing tables: {', '.join(missing)}")
        else:
            logger.info("✅ All expected tables present")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creating tables: {e}")
        return False


def initialize_database():
    """Main initialization function."""
    logger.info("=" * 70)
    logger.info("🚀 Production Database Initialization")
    logger.info("=" * 70)
    
    # Step 1: Check database connection
    logger.info("\n📡 Step 1: Checking database connection...")
    if not check_database_connection():
        logger.error("❌ Cannot connect to database. Please check DATABASE_URL environment variable.")
        sys.exit(1)
    
    # Step 2: Check existing tables
    logger.info("\n📋 Step 2: Checking existing tables...")
    existing_tables = check_existing_tables()
    
    # Step 3: Create tables
    logger.info("\n🏗️  Step 3: Creating database schema...")
    if create_tables():
        logger.info("\n✅ Database initialization completed successfully!")
        logger.info("\n📊 Next steps:")
        logger.info("1. Seed the database with sample data:")
        logger.info("   POST /api/v1/data/seed")
        logger.info("   Body: {\"num_vehicles\": 100, \"num_sales\": 10000, \"months_back\": 24}")
        logger.info("\n2. Or use the API documentation:")
        logger.info("   Visit: https://your-api.onrender.com/docs")
    else:
        logger.error("\n❌ Database initialization failed!")
        sys.exit(1)
    
    logger.info("\n" + "=" * 70)


if __name__ == "__main__":
    try:
        initialize_database()
    except KeyboardInterrupt:
        logger.info("\n⚠️  Initialization cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

