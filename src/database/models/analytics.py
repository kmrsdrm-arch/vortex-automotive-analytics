"""Analytics models for pre-computed metrics and insights."""

from sqlalchemy import Column, Integer, String, DateTime, Index, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from src.database.models.base import Base


class AnalyticsSnapshot(Base):
    """Model for storing pre-computed analytics snapshots."""

    __tablename__ = "analytics_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    snapshot_date = Column(DateTime(timezone=True), nullable=False, index=True)
    metric_type = Column(String(100), nullable=False, index=True)  # sales, inventory, kpi, etc.
    metric_data = Column(JSONB, nullable=False)  # Store computed metrics as JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (Index("idx_snapshot_date_type", "snapshot_date", "metric_type"),)

    def __repr__(self):
        return f"<AnalyticsSnapshot(id={self.id}, type='{self.metric_type}', date={self.snapshot_date})>"


class InsightHistory(Base):
    """Model for storing LLM-generated insights."""

    __tablename__ = "insight_history"

    id = Column(Integer, primary_key=True, index=True)
    insight_text = Column(Text, nullable=False)
    insight_type = Column(
        String(50), nullable=False, index=True
    )  # trend, anomaly, recommendation, etc.
    generated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    insight_metadata = Column(JSONB, nullable=True)  # Store additional context (date range, model used, etc.)

    __table_args__ = (Index("idx_type_generated", "insight_type", "generated_at"),)

    def __repr__(self):
        return f"<InsightHistory(id={self.id}, type='{self.insight_type}', generated={self.generated_at})>"

