"""Dependency injection for FastAPI."""

from typing import Generator
from sqlalchemy.orm import Session
from config.database import SessionLocal
from src.utils.logger import get_logger

logger = get_logger(__name__)


def get_db() -> Generator[Session, None, None]:
    """Database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

