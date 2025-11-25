"""Vehicle model."""

from sqlalchemy import Column, Integer, String, Numeric, DateTime, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from src.database.models.base import Base


class Vehicle(Base):
    """Vehicle model representing the automotive catalog."""

    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    vin = Column(String(17), unique=True, nullable=False, index=True)
    make = Column(String(50), nullable=False, index=True)
    model = Column(String(100), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)  # sedan, suv, truck, etc.
    trim = Column(String(100), nullable=True)
    msrp = Column(Numeric(10, 2), nullable=False)
    specifications = Column(JSONB, nullable=True)  # Store additional specs as JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Create composite indexes for common queries
    __table_args__ = (
        Index("idx_make_model", "make", "model"),
        Index("idx_category_year", "category", "year"),
    )

    def __repr__(self):
        return f"<Vehicle(id={self.id}, make='{self.make}', model='{self.model}', year={self.year})>"

