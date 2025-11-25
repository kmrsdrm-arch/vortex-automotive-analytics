"""
===================================================================================
Logging Utilities
===================================================================================

This module provides a simple, consistent way to get logger instances throughout
the application.

What is a Logger?
-----------------
A logger is an object that records messages about what's happening in your
application. Think of it like a diary that automatically writes entries when
important events occur.

Log messages help you:
- Debug issues (what went wrong?)
- Monitor performance (how fast is it?)
- Track usage (who's doing what?)
- Audit actions (security and compliance)

Why Use get_logger()?
---------------------
Instead of creating loggers directly in every file, we use this helper function
to ensure:
- Consistent logger naming (uses module name)
- Proper configuration (from config/logging_config.py)
- Easy to mock in tests
- Centralized logging setup

Author: Automotive Analytics Team
Version: 2.0.0
===================================================================================
"""

import logging


# ===================================================================================
# LOGGER FACTORY FUNCTION
# ===================================================================================

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    This is a simple factory function that creates/retrieves loggers with
    consistent naming and configuration.
    
    What is __name__?
    -----------------
    In Python, __name__ is a special variable that contains the module's
    full import path. For example:
    - In src/api/main.py: __name__ = "src.api.main"
    - In src/llm/core/client.py: __name__ = "src.llm.core.client"
    
    Using __name__ as the logger name makes it easy to identify which
    module generated each log message.
    
    Usage Pattern:
    --------------
    At the top of any module:
    ```python
    from src.utils.logger import get_logger
    
    logger = get_logger(__name__)  # Pass module name
    ```
    
    Then use the logger throughout the module:
    ```python
    logger.debug("Starting processing...")
    logger.info("User logged in successfully")
    logger.warning("API rate limit approaching")
    logger.error("Database connection failed", exc_info=True)
    logger.critical("System out of memory!")
    ```
    
    Log Levels:
    -----------
    - DEBUG: Detailed diagnostic information for debugging
      * Example: "Function called with arguments: x=5, y=10"
      * Use during development, turn off in production
    
    - INFO: General informational messages about normal operations
      * Example: "API server started on port 8000"
      * Default level for production
    
    - WARNING: Warning messages for unexpected but recoverable situations
      * Example: "Deprecated API endpoint used"
      * Something to be aware of but not critical
    
    - ERROR: Error messages for failures that should be investigated
      * Example: "Failed to process payment for order #12345"
      * Something went wrong but application continues
    
    - CRITICAL: Critical failures requiring immediate attention
      * Example: "Database connection pool exhausted"
      * Application may not function properly
    
    How Logging Configuration Works:
    ---------------------------------
    1. This function calls logging.getLogger(name)
    2. Python's logging system checks if logger with this name exists
    3. If not, creates new logger as child of root logger
    4. Logger inherits configuration from root logger (set in config/logging_config.py)
    5. Returns logger instance
    
    Logger Hierarchy:
    -----------------
    Loggers form a hierarchy based on dot-separated names:
    
    Root Logger (configured in config/logging_config.py)
    ├── src
    │   ├── src.api
    │   │   ├── src.api.main
    │   │   ├── src.api.middleware
    │   │   └── src.api.routes
    │   ├── src.llm
    │   │   └── src.llm.core
    │   └── src.database
    
    Child loggers inherit parent settings (level, handlers, formatters).
    You can override settings for specific subtrees if needed.
    
    Parameters:
    -----------
    name : str
        Name for the logger, typically __name__ (module import path).
        Examples:
        - "src.api.main"
        - "src.llm.core.client"
        - "src.database.models.vehicle"
    
    Returns:
    --------
    logging.Logger
        Configured logger instance ready to use.
        
        The logger has methods:
        - .debug(msg, *args, **kwargs): Debug level
        - .info(msg, *args, **kwargs): Info level
        - .warning(msg, *args, **kwargs): Warning level
        - .error(msg, *args, **kwargs): Error level
        - .critical(msg, *args, **kwargs): Critical level
        - .exception(msg, *args, **kwargs): Error with full traceback
    
    Example Usage:
    --------------
    ```python
    # In src/api/routes/analytics.py
    from src.utils.logger import get_logger
    
    # Create logger with module name
    logger = get_logger(__name__)  # Logger name: "src.api.routes.analytics"
    
    @router.get("/sales")
    def get_sales(db: Session = Depends(get_db)):
        logger.info("Fetching sales data")
        
        try:
            sales = db.query(Sale).all()
            logger.info(f"Retrieved {len(sales)} sales records")
            return sales
            
        except Exception as e:
            logger.error(f"Failed to fetch sales: {e}", exc_info=True)
            raise
    ```
    
    Log Output Example:
    -------------------
    2024-11-25 14:30:45 - src.api.routes.analytics - INFO - Fetching sales data
    2024-11-25 14:30:46 - src.api.routes.analytics - INFO - Retrieved 150 sales records
    
    Best Practices:
    ---------------
    1. Always use get_logger(__name__) at module level
       ✅ logger = get_logger(__name__)
       ❌ logger = logging.getLogger("my_logger")
    
    2. Include context in log messages
       ✅ logger.error(f"Failed to process order {order_id}: {str(e)}")
       ❌ logger.error("Error")
    
    3. Use appropriate log levels
       - DEBUG: Only during development
       - INFO: Normal operations worth noting
       - WARNING: Unexpected but handled
       - ERROR: Failures requiring investigation
       - CRITICAL: System-wide failures
    
    4. Use exc_info=True for exception details
       ✅ logger.error("Process failed", exc_info=True)
       ❌ logger.error(f"Process failed: {str(e)}")
    
    5. Don't log sensitive data
       ❌ logger.info(f"User login: {email} / {password}")
       ✅ logger.info(f"User login successful: {email}")
    
    Performance Considerations:
    ---------------------------
    - Logger creation is cheap (cached by name)
    - Calling get_logger multiple times with same name returns same instance
    - Log message formatting only happens if level is enabled
    - Use lazy formatting: logger.debug("Value: %s", value)
      instead of: logger.debug(f"Value: {value}")
    
    Thread Safety:
    --------------
    Python's logging module is thread-safe. Multiple threads can safely
    use the same logger without synchronization.
    """
    return logging.getLogger(name)

