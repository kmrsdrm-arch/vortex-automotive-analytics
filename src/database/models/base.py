"""
===================================================================================
Base Database Model Classes
===================================================================================

This module provides the foundation for all database models in the application.
It includes:
- Base: The declarative base class all models inherit from
- TimestampMixin: Reusable timestamp columns for created_at/updated_at

What is SQLAlchemy?
-------------------
SQLAlchemy is an ORM (Object-Relational Mapping) library that lets you:
- Define database tables as Python classes
- Query databases using Python objects instead of SQL
- Automatically handle type conversions
- Manage relationships between tables

ORM Benefits:
-------------
✅ Write Python instead of SQL
✅ Type-safe queries (IDE autocomplete works)
✅ Automatic SQL injection prevention
✅ Database-agnostic (works with PostgreSQL, MySQL, SQLite, etc.)
✅ Relationships handled automatically

Author: Automotive Analytics Team
Version: 2.0.0
===================================================================================
"""

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


# ===================================================================================
# DECLARATIVE BASE
# ===================================================================================

Base = declarative_base()
"""
The declarative base class for all database models.

What is Declarative Base?
--------------------------
It's the foundation class that all database models inherit from.
Think of it as the "parent" of all your database tables.

When you create a model like this:
    class User(Base):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True)
        name = Column(String)

SQLAlchemy:
1. Knows it's a database table (because it inherits Base)
2. Creates the table structure
3. Generates SQL queries automatically
4. Handles object persistence

Benefits:
---------
✅ Single source of truth for database schema
✅ Automatic table creation (Base.metadata.create_all())
✅ Relationship handling
✅ Query generation

Usage:
------
All models in src/database/models/ inherit from this Base class:
- models/vehicle.py: Vehicle model
- models/sales.py: Sale model
- models/inventory.py: Inventory model
- models/analytics.py: Analytics model

Example:
--------
```python
from src.database.models.base import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Decimal(10, 2))
```

This automatically creates a 'products' table in the database with three columns.
"""


# ===================================================================================
# TIMESTAMP MIXIN
# ===================================================================================

class TimestampMixin:
    """
    Mixin class for adding automatic timestamp columns to models.
    
    What is a Mixin?
    ----------------
    A mixin is a class that provides functionality to other classes through
    inheritance, but isn't meant to stand alone.
    
    Think of it like a "plugin" you can add to any model to give it
    timestamp tracking capabilities.
    
    Why Use a Mixin?
    ----------------
    Instead of copy-pasting created_at/updated_at columns to every model,
    you write them once here and reuse them everywhere.
    
    ❌ Without Mixin (repetitive):
    ```python
    class User(Base):
        id = Column(Integer, primary_key=True)
        created_at = Column(DateTime, server_default=func.now())
        updated_at = Column(DateTime, onupdate=func.now())
    
    class Product(Base):
        id = Column(Integer, primary_key=True)
        created_at = Column(DateTime, server_default=func.now())
        updated_at = Column(DateTime, onupdate=func.now())
    ```
    
    ✅ With Mixin (DRY - Don't Repeat Yourself):
    ```python
    class User(Base, TimestampMixin):
        id = Column(Integer, primary_key=True)
        # created_at and updated_at automatically added!
    
    class Product(Base, TimestampMixin):
        id = Column(Integer, primary_key=True)
        # created_at and updated_at automatically added!
    ```
    
    Columns Added:
    --------------
    - created_at: Timestamp when record was first created
    - updated_at: Timestamp when record was last modified
    
    Automatic Behavior:
    -------------------
    - created_at: Set automatically when you insert a row (never changes)
    - updated_at: Set automatically on insert AND updated on every change
    
    Usage:
    ------
    To add timestamps to any model, just inherit from TimestampMixin:
    
    ```python
    class Vehicle(Base, TimestampMixin):
        __tablename__ = "vehicles"
        id = Column(Integer, primary_key=True)
        make = Column(String(50))
        # Now has created_at and updated_at columns automatically!
    ```
    
    Database Queries:
    -----------------
    ```python
    # Find vehicles created in the last 24 hours
    recent = db.query(Vehicle).filter(
        Vehicle.created_at >= datetime.now() - timedelta(days=1)
    ).all()
    
    # Find vehicles modified today
    today = db.query(Vehicle).filter(
        Vehicle.updated_at >= datetime.now().date()
    ).all()
    ```
    
    Benefits:
    ---------
    ✅ Track when records were created
    ✅ Track when records were last modified
    ✅ Useful for auditing and debugging
    ✅ Reusable across all models
    ✅ Automatic (no manual timestamp management)
    """
    
    created_at = Column(
        DateTime(timezone=True),    # Use timezone-aware datetime
        server_default=func.now(),  # Database sets this automatically on INSERT
        nullable=False              # This field is required (cannot be NULL)
    )
    """
    Timestamp when the record was first created.
    
    Configuration:
    --------------
    - DateTime(timezone=True): Store with timezone info (UTC recommended)
    - server_default=func.now(): Database automatically sets current time
    - nullable=False: This field is required (every record has a created time)
    
    What is server_default?
    -----------------------
    Instead of Python code setting the timestamp, the DATABASE does it.
    This is better because:
    - More accurate (no network delay)
    - Works even if Python code forgets to set it
    - Consistent timezone handling
    - Faster (one database round-trip instead of two)
    
    What is func.now()?
    -------------------
    It's SQLAlchemy's way of saying "use the database's current timestamp function".
    - PostgreSQL: NOW()
    - MySQL: NOW()
    - SQLite: CURRENT_TIMESTAMP
    
    SQLAlchemy translates func.now() to the correct SQL for your database.
    
    Example:
    --------
    ```python
    # Create a new vehicle
    vehicle = Vehicle(make="Toyota", model="Camry")
    db.add(vehicle)
    db.commit()
    
    # created_at is automatically set by database
    print(vehicle.created_at)  # 2024-11-25 14:30:45.123456+00:00
    ```
    
    Behavior:
    ---------
    - Set once when record is created
    - Never changes after that (immutable)
    - Useful for sorting by age, filtering by creation date
    - Audit trail: Know when every record entered the system
    """
    
    updated_at = Column(
        DateTime(timezone=True),    # Use timezone-aware datetime
        server_default=func.now(),  # Database sets this on INSERT
        onupdate=func.now(),        # Database updates this on UPDATE
        nullable=False              # This field is required
    )
    """
    Timestamp when the record was last modified.
    
    Configuration:
    --------------
    - DateTime(timezone=True): Store with timezone info
    - server_default=func.now(): Set automatically on creation
    - onupdate=func.now(): Update automatically on every UPDATE query
    - nullable=False: This field is required
    
    What is onupdate?
    -----------------
    Tells the database: "Every time this row is updated, automatically
    refresh this column to the current timestamp".
    
    This happens automatically - you don't need to manually set updated_at!
    
    Example:
    --------
    ```python
    # Create a vehicle
    vehicle = Vehicle(make="Toyota", model="Camry")
    db.add(vehicle)
    db.commit()
    print(vehicle.created_at)   # 2024-11-25 14:30:45
    print(vehicle.updated_at)   # 2024-11-25 14:30:45 (same as created_at initially)
    
    # Later, update the vehicle
    vehicle.model = "Corolla"
    db.commit()
    print(vehicle.created_at)   # 2024-11-25 14:30:45 (unchanged)
    print(vehicle.updated_at)   # 2024-11-25 15:45:22 (automatically updated!)
    ```
    
    Use Cases:
    ----------
    - Find recently modified records
    - Cache invalidation (if updated_at changed, refresh cache)
    - Conflict detection (optimistic locking)
    - Audit trail (know when data last changed)
    - Data freshness (how old is this information?)
    
    Query Examples:
    ---------------
    ```python
    # Find records modified in the last hour
    from datetime import datetime, timedelta
    recent = db.query(Vehicle).filter(
        Vehicle.updated_at >= datetime.now() - timedelta(hours=1)
    ).all()
    
    # Sort by most recently modified
    latest = db.query(Vehicle).order_by(
        Vehicle.updated_at.desc()
    ).limit(10).all()
    ```
    
    Behavior:
    ---------
    - Set when record is created (same as created_at initially)
    - Automatically updated every time the record changes
    - Useful for cache invalidation, change tracking, audit logs
    """


