"""Database session management."""

from contextlib import contextmanager
from sqlalchemy.orm import Session
from config.database import SessionLocal
from src.utils.logger import get_logger

logger = get_logger(__name__)


@contextmanager
def get_db():
    """Context manager for database sessions."""
    db: Session = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def get_db_dependency():
    """Dependency for FastAPI route handlers."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

