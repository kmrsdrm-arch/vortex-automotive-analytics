"""
===================================================================================
Database Configuration and Connection Management
===================================================================================

This module provides centralized database configuration using SQLAlchemy.
It handles:
- Database engine creation with connection pooling
- Session management and lifecycle
- Dependency injection for FastAPI routes
- Connection health monitoring

Key Concepts:
-------------
1. Engine: Low-level database connection manager (singleton)
2. SessionLocal: Factory for creating database sessions
3. get_db(): FastAPI dependency for automatic session management

Author: Automotive Analytics Team
Version: 2.0.0
===================================================================================
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings


# ===================================================================================
# DATABASE ENGINE CONFIGURATION
# ===================================================================================

engine = create_engine(
    settings.database_url,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_pre_ping=True,
    echo=settings.debug,
)
"""
SQLAlchemy database engine with production-ready connection pooling.

Connection Pooling:
-------------------
- pool_size: Number of persistent connections maintained (default: 10)
    * These connections stay open and are reused across requests
    * Improves performance by avoiding repeated connection overhead
    * Increase for high-concurrency applications
    
- max_overflow: Additional connections allowed when pool is full (default: 20)
    * Total max connections = pool_size + max_overflow (10 + 20 = 30)
    * Overflow connections are created on-demand and closed after use
    * Prevents connection exhaustion during traffic spikes
    
- pool_pre_ping: Test connection health before using (default: True)
    * Automatically detects and discards stale connections
    * Prevents "connection lost" errors after long idle periods
    * Small overhead but critical for reliability
    
- echo: Log all SQL queries (default: False, True in debug mode)
    * Development: Helps debug query issues
    * Production: Keep False for performance

Performance Characteristics:
----------------------------
- Connection acquisition: < 1ms (from pool)
- Connection creation: 50-100ms (when pool exhausted)
- Pool exhaustion: Blocks until connection available
- Stale connection detection: Automatic via pool_pre_ping

Example Usage:
--------------
    # The engine is used internally by SessionLocal
    # You typically don't interact with it directly
    from config.database import engine
    
    # Check if database is reachable
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
"""


# ===================================================================================
# SESSION FACTORY
# ===================================================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
"""
Factory for creating database sessions.

Session Configuration:
----------------------
- autocommit=False: Changes are not committed automatically
    * Gives full control over transaction boundaries
    * Required for proper error handling and rollbacks
    * Must explicitly call session.commit() to persist changes
    
- autoflush=False: Changes are not flushed to DB automatically
    * Prevents unexpected SQL queries during object access
    * Improves performance by batching operations
    * You control when SQL is generated and executed
    
- bind=engine: Connects sessions to the configured engine
    * All sessions use the connection pool from 'engine'

Transaction Pattern:
--------------------
    session = SessionLocal()
    try:
        # Perform database operations
        user = session.query(User).filter_by(id=1).first()
        user.name = "Updated"
        
        # Explicitly commit to persist changes
        session.commit()
        
    except Exception as e:
        # Rollback on error to maintain data integrity
        session.rollback()
        raise e
        
    finally:
        # Always close session to return connection to pool
        session.close()

Note: In FastAPI routes, use the get_db() dependency instead of creating
      sessions manually. It handles all lifecycle management automatically.
"""


# ===================================================================================
# DATABASE SESSION DEPENDENCY
# ===================================================================================

def get_db():
    """
    FastAPI dependency for automatic database session management.
    
    This generator function:
    1. Creates a new database session
    2. Yields it to the route handler
    3. Automatically closes it when the request completes (or fails)
    
    Usage in FastAPI Routes:
    ------------------------
    ```python
    from fastapi import Depends
    from sqlalchemy.orm import Session
    from config.database import get_db
    
    @app.get("/users/{user_id}")
    def get_user(user_id: int, db: Session = Depends(get_db)):
        # db is automatically created and will be closed after return
        user = db.query(User).filter(User.id == user_id).first()
        return user
    ```
    
    Transaction Management:
    -----------------------
    - Session is created at the start of each request
    - Committed/rolled back within your route logic
    - Always closed after response is sent (even if exception occurs)
    - Connection returned to pool for reuse
    
    Benefits:
    ---------
    ✅ Automatic resource cleanup
    ✅ No connection leaks
    ✅ Consistent error handling
    ✅ Efficient connection pooling
    ✅ Thread-safe per-request sessions
    
    Error Handling:
    ---------------
    If an unhandled exception occurs in the route:
    - Session is automatically rolled back
    - Session is closed
    - Connection returned to pool
    - Exception propagates to FastAPI error handlers
    
    Yields:
    -------
    Session: SQLAlchemy database session for the current request
    
    Example with Transaction:
    --------------------------
    ```python
    @app.post("/users/")
    def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
        try:
            # Create new user
            new_user = User(**user_data.dict())
            db.add(new_user)
            
            # Commit to persist
            db.commit()
            db.refresh(new_user)  # Get generated ID
            
            return new_user
            
        except IntegrityError:
            # Rollback on duplicate/constraint violation
            db.rollback()
            raise HTTPException(status_code=400, detail="User already exists")
    ```
    """
    # Create a new session for this request
    db = SessionLocal()
    
    try:
        # Yield session to the route handler
        # Everything between try and finally is the route execution
        yield db
        
    finally:
        # This ALWAYS executes, even if route raises an exception
        # Ensures connection is returned to pool
        db.close()


# ===================================================================================
# CONNECTION HEALTH CHECK
# ===================================================================================

def check_database_connection() -> bool:
    """
    Verify database connectivity.
    
    Used for:
    - Startup health checks
    - Monitoring and alerting
    - Debugging connection issues
    
    Returns:
    --------
    bool: True if database is reachable and responding, False otherwise
    
    Example:
    --------
    ```python
    from config.database import check_database_connection
    
    if not check_database_connection():
        logger.error("Database is not reachable!")
        sys.exit(1)
    ```
    """
    try:
        # Try to establish connection and run simple query
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
        
    except Exception as e:
        # Log the error for debugging
        import logging
        logging.error(f"Database connection check failed: {e}")
        return False

