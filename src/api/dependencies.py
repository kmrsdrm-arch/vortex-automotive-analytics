"""
===================================================================================
FastAPI Dependency Injection System
===================================================================================

This module provides reusable dependencies for FastAPI endpoints using
Dependency Injection pattern.

What is Dependency Injection?
------------------------------
Instead of creating resources (like database connections) inside each endpoint,
we "inject" them from outside. This provides:
- Reusability: Same dependency used across multiple endpoints
- Testability: Easy to mock dependencies in tests
- Separation: Business logic separate from resource management
- Automatic cleanup: Resources properly closed after use

How FastAPI Dependencies Work:
-------------------------------
1. Define a function that creates/yields a resource
2. Add it to endpoint with Depends()
3. FastAPI calls function before endpoint
4. Passes result to endpoint as parameter
5. Runs cleanup code after endpoint finishes

Example:
--------
```python
from fastapi import Depends
from sqlalchemy.orm import Session
from src.api.dependencies import get_db

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    # db is automatically created and injected here
    users = db.query(User).all()
    return users
    # db is automatically closed after this function returns
```

Benefits of This Pattern:
--------------------------
✅ No manual connection management
✅ Automatic resource cleanup
✅ Easy to test (mock dependencies)
✅ Type-safe (IDE autocomplete works)
✅ Consistent error handling

Common Dependencies:
--------------------
- Database sessions (get_db)
- Authentication (get_current_user)
- Authorization (require_admin)
- Rate limiting (rate_limit)
- Caching (cache_response)

Author: Automotive Analytics Team
Version: 2.0.0
===================================================================================
"""

from typing import Generator
from sqlalchemy.orm import Session
from config.database import SessionLocal
from src.utils.logger import get_logger

logger = get_logger(__name__)


# ===================================================================================
# DATABASE SESSION DEPENDENCY
# ===================================================================================

def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency for FastAPI endpoints.
    
    This is a generator function that:
    1. Creates a database session
    2. Yields it to the endpoint
    3. Automatically closes it after the endpoint finishes
    
    What is a Generator?
    --------------------
    A generator is a special function that can pause and resume execution.
    The `yield` statement pauses the function and returns a value.
    Code after `yield` runs after the endpoint completes.
    
    Execution Flow:
    ---------------
    1. FastAPI calls get_db()
    2. Session created: db = SessionLocal()
    3. Enters try block
    4. Yields db (pauses here, passes to endpoint)
    5. --- Endpoint code runs here ---
    6. Resumes after endpoint returns
    7. Finally block executes
    8. Session closed: db.close()
    
    Usage in FastAPI Endpoints:
    ----------------------------
    ```python
    from fastapi import APIRouter, Depends
    from sqlalchemy.orm import Session
    from src.api.dependencies import get_db
    
    router = APIRouter()
    
    @router.get("/users")
    def get_users(db: Session = Depends(get_db)):
        # Database session automatically provided
        users = db.query(User).all()
        return users
        # Session automatically closed when function returns
    ```
    
    Error Handling:
    ---------------
    If the endpoint raises an exception:
    1. Exception propagates up
    2. Finally block STILL executes
    3. Session is closed properly
    4. No connection leaks
    
    This ensures connections are always returned to the pool, even if
    errors occur.
    
    Why Not Create Session Directly in Endpoint?
    ---------------------------------------------
    ❌ Manual approach (error-prone):
    ```python
    @app.get("/users")
    def get_users():
        db = SessionLocal()  # Must remember to do this
        try:
            users = db.query(User).all()
            return users
        finally:
            db.close()  # Must remember to do this
    ```
    
    ✅ Dependency injection (automatic):
    ```python
    @app.get("/users")
    def get_users(db: Session = Depends(get_db)):
        users = db.query(User).all()
        return users
        # Cleanup handled automatically!
    ```
    
    Connection Pooling:
    -------------------
    SessionLocal uses a connection pool (configured in config/database.py):
    - Pool size: 10 connections kept open
    - Max overflow: 20 additional connections
    - Total max: 30 concurrent connections
    
    When you call db.close():
    - Connection is NOT actually closed
    - It's returned to the pool for reuse
    - Next request reuses existing connection (fast!)
    
    Performance:
    ------------
    - Getting connection from pool: <1ms
    - Creating new connection: 50-100ms
    - Pooling provides ~50-100x speedup
    
    Thread Safety:
    --------------
    Each request gets its own session. Sessions are NOT shared between
    requests, so there's no risk of race conditions or concurrent access
    issues.
    
    Yields:
    -------
    Session: SQLAlchemy database session
        - Connected to PostgreSQL database
        - Ready for queries and transactions
        - Automatically closed after use
    
    Raises:
    -------
    No exceptions raised directly, but endpoint code using the session
    might raise database-related exceptions like:
    - sqlalchemy.exc.IntegrityError: Constraint violation
    - sqlalchemy.exc.OperationalError: Connection failure
    - sqlalchemy.exc.DataError: Invalid data
    """
    # Create a new database session from the connection pool
    db = SessionLocal()
    
    try:
        # Yield session to the endpoint
        # Execution pauses here and passes control to the endpoint
        yield db
        
        # After endpoint completes, execution resumes here
        # If endpoint raised exception, we skip this and go to finally
        
    finally:
        # This ALWAYS executes, even if endpoint raised an exception
        # Close session (returns connection to pool)
        db.close()
        logger.debug("Database session closed and returned to pool")

