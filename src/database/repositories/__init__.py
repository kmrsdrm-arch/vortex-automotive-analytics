"""Repository pattern implementation for data access."""

from src.database.repositories.base import BaseRepository
from src.database.repositories.vehicle_repo import VehicleRepository
from src.database.repositories.inventory_repo import InventoryRepository
from src.database.repositories.sales_repo import SalesRepository

__all__ = ["BaseRepository", "VehicleRepository", "InventoryRepository", "SalesRepository"]

