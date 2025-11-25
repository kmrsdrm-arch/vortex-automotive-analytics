"""Inventory model."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.database.models.base import Base


class Inventory(Base):
    """Inventory model representing vehicle stock levels."""

    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)
    warehouse_location = Column(String(200), nullable=False, index=True)
    region = Column(String(100), nullable=False, index=True)
    quantity_available = Column(Integer, nullable=False, default=0)
    quantity_reserved = Column(Integer, nullable=False, default=0)
    reorder_point = Column(Integer, nullable=False, default=10)
    last_restocked = Column(DateTime(timezone=True), nullable=True)
    status = Column(
        String(20), nullable=False, default="active", index=True
    )  # active, low, out_of_stock
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationship
    vehicle = relationship("Vehicle", backref="inventory_records")

    # Constraints
    __table_args__ = (
        CheckConstraint("quantity_available >= 0", name="check_quantity_available_positive"),
        CheckConstraint("quantity_reserved >= 0", name="check_quantity_reserved_positive"),
        Index("idx_vehicle_warehouse", "vehicle_id", "warehouse_location"),
        Index("idx_region_status", "region", "status"),
    )

    def __repr__(self):
        return f"<Inventory(id={self.id}, vehicle_id={self.vehicle_id}, location='{self.warehouse_location}', qty={self.quantity_available})>"

