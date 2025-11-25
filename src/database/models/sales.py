"""Sales model."""

from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Index, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.database.models.base import Base


class Sales(Base):
    """Sales model representing sales transactions."""

    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)
    sale_date = Column(Date, nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)
    customer_segment = Column(
        String(50), nullable=False, index=True
    )  # individual, fleet, dealer
    region = Column(String(100), nullable=False, index=True)
    salesperson_id = Column(String(50), nullable=True)
    discount_applied = Column(Numeric(5, 2), nullable=False, default=0.0)  # Percentage
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship
    vehicle = relationship("Vehicle", backref="sales_records")

    # Indexes for common queries
    __table_args__ = (
        Index("idx_sale_date_region", "sale_date", "region"),
        Index("idx_vehicle_sale_date", "vehicle_id", "sale_date"),
        Index("idx_customer_segment_date", "customer_segment", "sale_date"),
    )

    def __repr__(self):
        return f"<Sales(id={self.id}, vehicle_id={self.vehicle_id}, date={self.sale_date}, amount=${self.total_amount})>"

