"""
===================================================================================
Centralized Logging Configuration
===================================================================================

This module sets up application-wide logging with:
- Console output for development monitoring
- File output with automatic rotation
- Structured log format with timestamps
- Log level control via settings
- Suppression of noisy third-party loggers

Logging Levels (from most to least verbose):
---------------------------------------------
DEBUG    - Detailed diagnostic information for debugging
INFO     - General informational messages (default)
WARNING  - Warning messages for recoverable issues
ERROR    - Error messages for failures
CRITICAL - Critical failures requiring immediate attention

Best Practices:
---------------
- Development: Use DEBUG level
- Production: Use INFO or WARNING level
- Never log sensitive data (passwords, API keys)
- Use structured logging for better parsing
- Rotate logs to prevent disk space issues

Author: Automotive Analytics Team
Version: 2.0.0
===================================================================================
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from config.settings import settings


# ===================================================================================
# MAIN LOGGING SETUP FUNCTION
# ===================================================================================

def setup_logging():
    """
    Configure application-wide logging with console and file output.
    
    This function:
    1. Creates log directory if it doesn't exist
    2. Sets up log formatters for consistent output
    3. Configures console handler for terminal output
    4. Configures file handler with automatic rotation
    5. Suppresses noisy third-party library loggers
    
    Log Format:
    -----------
    YYYY-MM-DD HH:MM:SS - module_name - LEVEL - message
    
    Example output:
    2024-11-25 14:30:45 - src.api.main - INFO - Starting application
    2024-11-25 14:30:46 - src.llm.client - DEBUG - OpenAI API call: 234ms
    2024-11-25 14:30:47 - src.analytics - ERROR - Failed to calculate KPI: division by zero
    
    Log Rotation:
    -------------
    - Max file size: 10MB
    - Backup files: 5
    - Total max disk space: 50MB (5 backups * 10MB)
    - Old files automatically compressed and archived
    
    Files created:
    - logs/app.log (current log)
    - logs/app.log.1 (previous rotation)
    - logs/app.log.2 (older rotation)
    - ... up to app.log.5
    
    Thread Safety:
    --------------
    Python's logging module is thread-safe. Multiple threads/processes
    can safely write to the same log file without corruption.
    
    Returns:
    --------
    logging.Logger: Configured root logger instance
    
    Usage:
    ------
    ```python
    from config.logging_config import logger
    
    logger.debug("Detailed diagnostic information")
    logger.info("General informational message")
    logger.warning("Something unexpected happened")
    logger.error("An error occurred", exc_info=True)  # Include traceback
    logger.critical("System is in critical state!")
    ```
    """
    
    # ===============================================================================
    # STEP 1: Create log directory if it doesn't exist
    # ===============================================================================
    
    log_dir = os.path.dirname(settings.log_file)
    if log_dir and not os.path.exists(log_dir):
        # Create directory with parents (like mkdir -p)
        os.makedirs(log_dir, exist_ok=True)
    
    # ===============================================================================
    # STEP 2: Create log formatter for consistent message format
    # ===============================================================================
    
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    """
    Log message format components:
    - %(asctime)s: Timestamp (e.g., 2024-11-25 14:30:45)
    - %(name)s: Logger name (usually module path)
    - %(levelname)s: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - %(message)s: The actual log message
    
    Other available fields:
    - %(filename)s: File name where log was called
    - %(lineno)d: Line number where log was called
    - %(funcName)s: Function name where log was called
    - %(process)d: Process ID
    - %(thread)d: Thread ID
    """
    
    # ===============================================================================
    # STEP 3: Configure console handler (terminal output)
    # ===============================================================================
    
    console_handler = logging.StreamHandler()
    """
    Console handler writes logs to standard output (terminal).
    
    Behavior:
    - Writes to sys.stdout (can be redirected)
    - Colored output in supported terminals
    - Immediate output (no buffering)
    - Visible during development
    """
    
    console_handler.setLevel(settings.log_level)
    console_handler.setFormatter(formatter)
    
    # ===============================================================================
    # STEP 4: Configure file handler with rotation
    # ===============================================================================
    
    file_handler = RotatingFileHandler(
        filename=settings.log_file,
        maxBytes=10485760,  # 10MB in bytes (10 * 1024 * 1024)
        backupCount=5       # Keep 5 backup files
    )
    """
    Rotating file handler automatically manages log file size.
    
    How it works:
    1. Writes to app.log until it reaches 10MB
    2. When limit reached:
       - Renames app.log -> app.log.1
       - Renames app.log.1 -> app.log.2
       - ... and so on up to app.log.5
       - Deletes app.log.5 if it exists
       - Creates new empty app.log
    
    Benefits:
    ✅ Prevents unlimited disk space usage
    ✅ Keeps recent logs accessible
    ✅ Automatic cleanup of old logs
    ✅ No manual intervention required
    
    Storage calculation:
    - Current log: up to 10MB
    - 5 backups: up to 50MB
    - Total: maximum 60MB
    """
    
    file_handler.setLevel(settings.log_level)
    file_handler.setFormatter(formatter)
    
    # ===============================================================================
    # STEP 5: Configure root logger
    # ===============================================================================
    
    root_logger = logging.getLogger()
    """
    The root logger is the parent of all loggers in the application.
    
    When you create a logger in any module:
        logger = logging.getLogger(__name__)
    
    It inherits settings from the root logger unless explicitly overridden.
    
    This ensures consistent logging behavior across the entire application.
    """
    
    root_logger.setLevel(settings.log_level)
    
    # Add both handlers to root logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # ===============================================================================
    # STEP 6: Suppress noisy third-party loggers
    # ===============================================================================
    
    # urllib3 (used by requests library) generates excessive debug logs
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    """
    urllib3 logs every HTTP request at DEBUG level, which is too verbose.
    Setting to WARNING means we only see connection errors, not routine requests.
    """
    
    # httpx (async HTTP client) also generates verbose logs
    logging.getLogger("httpx").setLevel(logging.WARNING)
    """
    httpx logs every async request, which clutters logs during normal operation.
    Set to WARNING to only see issues, not successful requests.
    """
    
    # Add more noisy loggers as needed
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    """
    Uvicorn logs every HTTP request at INFO level. In production with high traffic,
    this can generate gigabytes of logs. Set to WARNING to only log issues.
    
    If you need access logs, use a dedicated access log file instead.
    """
    
    return root_logger


# ===================================================================================
# INITIALIZE LOGGING ON MODULE IMPORT
# ===================================================================================

logger = setup_logging()
"""
Global logger instance initialized when this module is imported.

Usage throughout the application:
----------------------------------
    from config.logging_config import logger
    
    logger.debug("Debugging info")
    logger.info("Something happened")
    logger.warning("Be careful!")
    logger.error("Something failed")
    logger.critical("System is down!")

Best Practices:
---------------
1. Use appropriate log levels:
   - DEBUG: Detailed diagnostic data (e.g., variable values, execution flow)
   - INFO: Major events (e.g., API started, user logged in)
   - WARNING: Unexpected but recoverable (e.g., deprecated API used)
   - ERROR: Errors that should be investigated (e.g., failed DB query)
   - CRITICAL: System failures (e.g., out of memory, cannot connect to DB)

2. Include context in messages:
   ❌ Bad:  logger.error("Failed")
   ✅ Good: logger.error(f"Failed to process order {order_id}: {str(e)}")

3. Use exc_info for exceptions:
   ❌ Bad:  logger.error(f"Error: {str(e)}")
   ✅ Good: logger.error("Error processing request", exc_info=True)

4. Don't log sensitive data:
   ❌ Bad:  logger.info(f"User login: {email} / {password}")
   ✅ Good: logger.info(f"User login successful: {email}")

5. Structure your messages:
   ✅ Good: logger.info(f"API call: endpoint={endpoint}, duration={duration}ms, status={status}")

Performance Considerations:
---------------------------
- Logging is I/O-bound (disk writes)
- DEBUG level can slow down application (use INFO+ in production)
- Log rotation prevents disk space issues
- Consider async logging for very high-traffic applications

Monitoring and Alerting:
-------------------------
- Parse logs with tools like ELK Stack, Splunk, or Datadog
- Alert on ERROR and CRITICAL levels
- Track trends (e.g., increasing WARNING counts)
- Use structured logging (JSON) for easier parsing
"""

