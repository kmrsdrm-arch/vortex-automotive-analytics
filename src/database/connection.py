"""Database connection management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Create database engine
engine = create_engine(
    settings.database_url,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_pre_ping=True,
    echo=settings.debug,
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    """Get a database session."""
    session = SessionLocal()
    try:
        return session
    except Exception as e:
        logger.error(f"Error creating database session: {e}")
        raise


def close_db_session(session):
    """Close a database session."""
    try:
        session.close()
    except Exception as e:
        logger.error(f"Error closing database session: {e}")

