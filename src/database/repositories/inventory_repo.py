"""Inventory repository with stock management queries."""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from src.database.models.inventory import Inventory
from src.database.repositories.base import BaseRepository
from src.utils.logger import get_logger

logger = get_logger(__name__)


class InventoryRepository(BaseRepository[Inventory]):
    """Repository for Inventory operations."""

    def __init__(self, db: Session):
        super().__init__(Inventory, db)

    def get_by_vehicle_id(self, vehicle_id: int) -> List[Inventory]:
        """Get all inventory records for a vehicle."""
        try:
            return self.db.query(Inventory).filter(Inventory.vehicle_id == vehicle_id).all()
        except Exception as e:
            logger.error(f"Error fetching inventory for vehicle {vehicle_id}: {e}")
            raise

    def get_by_warehouse(self, warehouse_location: str) -> List[Inventory]:
        """Get inventory for a specific warehouse."""
        try:
            return (
                self.db.query(Inventory)
                .filter(Inventory.warehouse_location == warehouse_location)
                .all()
            )
        except Exception as e:
            logger.error(f"Error fetching inventory for warehouse {warehouse_location}: {e}")
            raise

    def get_by_region(self, region: str) -> List[Inventory]:
        """Get inventory for a specific region."""
        try:
            return self.db.query(Inventory).filter(Inventory.region == region).all()
        except Exception as e:
            logger.error(f"Error fetching inventory for region {region}: {e}")
            raise

    def get_low_stock_items(self) -> List[Inventory]:
        """Get items where available quantity is below reorder point."""
        try:
            return (
                self.db.query(Inventory)
                .filter(Inventory.quantity_available < Inventory.reorder_point)
                .all()
            )
        except Exception as e:
            logger.error(f"Error fetching low stock items: {e}")
            raise

    def get_out_of_stock_items(self) -> List[Inventory]:
        """Get items that are out of stock."""
        try:
            return self.db.query(Inventory).filter(Inventory.quantity_available == 0).all()
        except Exception as e:
            logger.error(f"Error fetching out of stock items: {e}")
            raise

    def get_by_status(self, status: str) -> List[Inventory]:
        """Get inventory by status."""
        try:
            return self.db.query(Inventory).filter(Inventory.status == status).all()
        except Exception as e:
            logger.error(f"Error fetching inventory by status {status}: {e}")
            raise

    def get_total_quantity_by_vehicle(self, vehicle_id: int) -> int:
        """Get total available quantity across all warehouses for a vehicle."""
        try:
            result = (
                self.db.query(func.sum(Inventory.quantity_available))
                .filter(Inventory.vehicle_id == vehicle_id)
                .scalar()
            )
            return result or 0
        except Exception as e:
            logger.error(f"Error calculating total quantity for vehicle {vehicle_id}: {e}")
            raise

    def update_stock(
        self, id: int, quantity_change: int, update_status: bool = True
    ) -> Optional[Inventory]:
        """Update stock quantity and optionally status."""
        try:
            inventory = self.get_by_id(id)
            if inventory:
                inventory.quantity_available += quantity_change
                inventory.last_restocked = datetime.utcnow()

                if update_status:
                    if inventory.quantity_available == 0:
                        inventory.status = "out_of_stock"
                    elif inventory.quantity_available < inventory.reorder_point:
                        inventory.status = "low"
                    else:
                        inventory.status = "active"

                self.db.commit()
                self.db.refresh(inventory)
                logger.debug(f"Updated stock for inventory id {id}")
            return inventory
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating stock for inventory id {id}: {e}")
            raise

