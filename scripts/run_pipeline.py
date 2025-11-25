"""Run ETL pipeline manually."""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import SessionLocal
from src.pipeline.pipeline_manager import PipelineManager
from config.logging_config import logger


def run_pipeline(days_back: int = 30):
    """Run the ETL pipeline."""
    db = SessionLocal()

    try:
        logger.info(f"Running ETL pipeline for last {days_back} days...")

        manager = PipelineManager(db)
        result = manager.run_full_pipeline(days_back=days_back)

        logger.info("=" * 50)
        logger.info("Pipeline Execution Summary:")
        logger.info(f"  Status: {result['status']}")
        if result.get('sales'):
            logger.info(f"  Sales Records Processed: {result['sales'].get('records_processed', 0)}")
        if result.get('inventory'):
            logger.info(f"  Inventory Records Processed: {result['inventory'].get('records_processed', 0)}")
        logger.info(f"  Completed At: {result['completed_at']}")
        logger.info("=" * 50)

    except Exception as e:
        logger.error(f"Error running pipeline: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run ETL pipeline")
    parser.add_argument("--days", type=int, default=30, help="Number of days to process")

    args = parser.parse_args()

    run_pipeline(days_back=args.days)

