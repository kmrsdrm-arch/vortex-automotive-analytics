"""Database models."""

from src.database.models.base import Base
from src.database.models.vehicle import Vehicle
from src.database.models.inventory import Inventory
from src.database.models.sales import Sales
from src.database.models.analytics import AnalyticsSnapshot, InsightHistory

__all__ = ["Base", "Vehicle", "Inventory", "Sales", "AnalyticsSnapshot", "InsightHistory"]

