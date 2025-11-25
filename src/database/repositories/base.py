"""Base repository with common CRUD operations."""

from typing import Generic, TypeVar, Type, List, Optional, Any
from sqlalchemy.orm import Session
from src.utils.logger import get_logger

logger = get_logger(__name__)

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """Base repository class with common CRUD operations."""

    def __init__(self, model: Type[ModelType], db: Session):
        """Initialize repository with model and database session."""
        self.model = model
        self.db = db

    def create(self, **kwargs) -> ModelType:
        """Create a new record."""
        try:
            instance = self.model(**kwargs)
            self.db.add(instance)
            self.db.commit()
            self.db.refresh(instance)
            logger.debug(f"Created {self.model.__name__} with id: {instance.id}")
            return instance
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating {self.model.__name__}: {e}")
            raise

    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Get a record by ID."""
        try:
            return self.db.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            logger.error(f"Error fetching {self.model.__name__} by id {id}: {e}")
            raise

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all records with pagination."""
        try:
            return self.db.query(self.model).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error fetching all {self.model.__name__}: {e}")
            raise

    def update(self, id: int, **kwargs) -> Optional[ModelType]:
        """Update a record by ID."""
        try:
            instance = self.get_by_id(id)
            if instance:
                for key, value in kwargs.items():
                    setattr(instance, key, value)
                self.db.commit()
                self.db.refresh(instance)
                logger.debug(f"Updated {self.model.__name__} with id: {id}")
            return instance
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating {self.model.__name__} id {id}: {e}")
            raise

    def delete(self, id: int) -> bool:
        """Delete a record by ID."""
        try:
            instance = self.get_by_id(id)
            if instance:
                self.db.delete(instance)
                self.db.commit()
                logger.debug(f"Deleted {self.model.__name__} with id: {id}")
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting {self.model.__name__} id {id}: {e}")
            raise

    def count(self) -> int:
        """Count total records."""
        try:
            return self.db.query(self.model).count()
        except Exception as e:
            logger.error(f"Error counting {self.model.__name__}: {e}")
            raise

    def bulk_create(self, objects: List[dict]) -> List[ModelType]:
        """Bulk create multiple records."""
        try:
            instances = [self.model(**obj) for obj in objects]
            self.db.bulk_save_objects(instances)
            self.db.commit()
            logger.debug(f"Bulk created {len(instances)} {self.model.__name__} records")
            return instances
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error bulk creating {self.model.__name__}: {e}")
            raise

