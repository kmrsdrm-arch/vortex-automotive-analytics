"""Data loading utilities."""

import pandas as pd
from sqlalchemy.orm import Session
from src.database.models import AnalyticsSnapshot
from datetime import datetime
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DataLoader:
    """Load processed data back to database."""

    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db

    def load_analytics_snapshot(
        self, metric_type: str, metric_data: dict, snapshot_date: datetime = None
    ) -> AnalyticsSnapshot:
        """Load analytics snapshot to database."""
        try:
            if snapshot_date is None:
                snapshot_date = datetime.now()

            snapshot = AnalyticsSnapshot(
                snapshot_date=snapshot_date, metric_type=metric_type, metric_data=metric_data
            )

            self.db.add(snapshot)
            self.db.commit()
            self.db.refresh(snapshot)

            logger.info(f"Loaded analytics snapshot: {metric_type}")
            return snapshot

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error loading analytics snapshot: {e}")
            raise

    def load_dataframe_to_analytics(
        self, df: pd.DataFrame, metric_type: str
    ) -> AnalyticsSnapshot:
        """Convert dataframe to JSON and load as analytics snapshot."""
        try:
            metric_data = df.to_dict(orient="records")
            return self.load_analytics_snapshot(metric_type, metric_data)

        except Exception as e:
            logger.error(f"Error loading dataframe to analytics: {e}")
            raise

    def export_to_csv(self, df: pd.DataFrame, filepath: str) -> None:
        """Export dataframe to CSV file."""
        try:
            df.to_csv(filepath, index=False)
            logger.info(f"Exported data to {filepath}")

        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            raise

    def export_to_json(self, df: pd.DataFrame, filepath: str) -> None:
        """Export dataframe to JSON file."""
        try:
            df.to_json(filepath, orient="records", indent=2)
            logger.info(f"Exported data to {filepath}")

        except Exception as e:
            logger.error(f"Error exporting to JSON: {e}")
            raise

