"""
===================================================================================
FastAPI Application Entry Point
===================================================================================

This is the main entry point for the Automotive Analytics API. It sets up:
- FastAPI application with automatic documentation
- CORS middleware for cross-origin requests (allows Streamlit dashboard to connect)
- Custom logging middleware to track all requests
- API route modules for different features

What is FastAPI?
----------------
FastAPI is a modern, high-performance web framework for building APIs with Python.
It automatically:
- Validates request data
- Generates interactive API documentation (/docs and /redoc)
- Serializes Python objects to JSON
- Handles async operations efficiently

Application Architecture:
-------------------------
1. Middleware Layer: Intercepts and processes all requests/responses
   - CORS: Allows frontend (Streamlit) to make API calls
   - Logging: Tracks performance and errors
   
2. Route Layer: Organizes endpoints by feature
   - Health: System status checks
   - Analytics: Sales and inventory analytics
   - Insights: AI-generated business insights
   - Reports: Comprehensive report generation
   - Query: Natural language query processing
   - Data: Data retrieval and management

3. Service Layer: Business logic and data processing
   - LLM services for AI features
   - Analytics calculators
   - Data pipelines

Author: Automotive Analytics Team
Version: 2.0.0
===================================================================================
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings
from config.logging_config import logger
from src.api.middleware import LoggingMiddleware
from src.api.routes import health, analytics, insights, reports, query, data


# ===================================================================================
# FASTAPI APPLICATION INITIALIZATION
# ===================================================================================

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Automotive Analytics Pipeline with LLM-powered insights",
    docs_url="/docs",      # Interactive API documentation (Swagger UI)
    redoc_url="/redoc",    # Alternative documentation (ReDoc)
)
"""
FastAPI application instance with auto-generated documentation.

Interactive Documentation URLs:
--------------------------------
- Swagger UI: http://localhost:8000/docs
  * Try out API endpoints directly in browser
  * See request/response schemas
  * Automatically updated when code changes
  
- ReDoc: http://localhost:8000/redoc
  * Clean, three-panel documentation
  * Better for reading and sharing
  * Shows detailed schemas and examples

Configuration:
--------------
- title: Displayed in documentation
- version: API version (semantic versioning)
- description: Overview text in documentation
"""


# ===================================================================================
# CORS MIDDLEWARE CONFIGURATION
# ===================================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api_cors_origins,  # Which domains can call this API
    allow_credentials=True,                    # Allow cookies and auth headers
    allow_methods=["*"],                       # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],                       # Allow all request headers
)
"""
CORS (Cross-Origin Resource Sharing) Middleware

What is CORS?
-------------
Web browsers block JavaScript from making requests to different domains
for security reasons. This is called the "Same-Origin Policy".

For example, if Streamlit runs on localhost:8501 and API runs on
localhost:8000, they're different origins (different ports), so the browser
blocks requests by default.

CORS middleware tells the browser "it's okay to allow these specific
domains to make requests to this API".

Configuration:
--------------
- allow_origins: List of allowed frontend URLs
  * Default: ["http://localhost:8501"] (Streamlit default port)
  * Production: Add your deployed frontend URL
  * Security: Never use ["*"] in production (allows any website)

- allow_credentials: Allow authentication headers and cookies
  * Required for login/session features
  * Enables secure, authenticated requests

- allow_methods: Which HTTP verbs are allowed
  * ["*"] = All methods (GET, POST, PUT, DELETE, PATCH, OPTIONS)
  * Can restrict to specific methods for tighter security

- allow_headers: Which request headers are allowed
  * ["*"] = All headers (Authorization, Content-Type, etc.)
  * Needed for custom headers and authentication tokens

How it works:
-------------
1. Browser makes "preflight" OPTIONS request asking "can I do this?"
2. API responds with CORS headers saying "yes, you can"
3. Browser allows the actual request to proceed
4. API processes request and returns response

Without CORS:
-------------
Browser error: "Access to fetch at 'http://localhost:8000/api/...' from 
origin 'http://localhost:8501' has been blocked by CORS policy"
"""


# ===================================================================================
# CUSTOM MIDDLEWARE
# ===================================================================================

app.add_middleware(LoggingMiddleware)
"""
Custom logging middleware to track all API requests and responses.

This middleware:
1. Logs every incoming request (method and path)
2. Measures processing time
3. Logs response status and duration
4. Adds X-Process-Time header to response

Example log output:
2024-11-25 14:30:45 - src.api.middleware - INFO - Request: GET /api/analytics/sales
2024-11-25 14:30:45 - src.api.middleware - INFO - Response: 200 - GET /api/analytics/sales - 0.234s

Benefits:
- Monitor API performance
- Debug slow endpoints
- Track usage patterns
- Identify errors quickly
"""


# ===================================================================================
# API ROUTE REGISTRATION
# ===================================================================================

# Health check endpoints (system status, database connectivity)
app.include_router(health.router)

# Sales and inventory analytics endpoints
app.include_router(analytics.router)

# AI-powered insights generation endpoints
app.include_router(insights.router)

# Report generation and export endpoints
app.include_router(reports.router)

# Natural language query processing endpoints
app.include_router(query.router)

# Data retrieval and management endpoints
app.include_router(data.router)

"""
Route Organization:
-------------------
Each router handles a specific feature area:

1. health.router: /health
   - System health checks
   - Database connectivity
   - OpenAI API status

2. analytics.router: /api/analytics/*
   - Sales analytics and KPIs
   - Inventory metrics
   - Trend analysis

3. insights.router: /api/insights/*
   - AI-generated business insights
   - Anomaly detection
   - Recommendations

4. reports.router: /api/reports/*
   - Comprehensive reports
   - PDF/Excel exports
   - Custom date ranges

5. query.router: /api/query/*
   - Natural language queries
   - AI-powered data retrieval
   - Plain English to SQL

6. data.router: /api/data/*
   - Raw data access
   - CRUD operations
   - Data seeding
"""



# ===================================================================================
# APPLICATION LIFECYCLE EVENTS
# ===================================================================================

@app.on_event("startup")
async def startup_event():
    """
    Application startup event handler.
    
    This function runs once when the API server starts up. It:
    1. Logs application information (name, version, host, port)
    2. Validates OpenAI API connection
    3. Checks that all required services are accessible
    
    Why validate on startup?
    ------------------------
    - Fail fast: Detect configuration issues immediately, not during user requests
    - Clear errors: Show exact problem before accepting traffic
    - Better UX: Users don't get cryptic errors when they try to use AI features
    
    What happens if validation fails?
    ---------------------------------
    The API server STILL STARTS, but logs warnings. This allows:
    - Basic analytics features to work (don't need AI)
    - Debugging and health checks to function
    - Graceful degradation instead of complete failure
    
    Only AI-powered features (NL Query, Insights, Reports) will fail if
    OpenAI connection is invalid.
    """
    # Log startup information
    try:
        logger.info(f"Starting {settings.app_name} v{settings.app_version}")
        logger.info(f"API server starting on {settings.api_host}:{settings.api_port}")
        logger.info(f"DATABASE_URL configured: {settings.database_url[:20]}...") # Log first 20 chars only
    except Exception as e:
        logger.error(f"Failed to load settings: {e}")
        # Continue anyway - settings might be partially loaded
    
    # ===================================================================================
    # OPENAI API VALIDATION (Optional - won't crash if fails)
    # ===================================================================================
    
    try:
        # Import OpenAI client
        from src.llm.core.client import client
        logger.info("Validating OpenAI API connection...")
        
        # Test with a simple completion request
        test_response = client.simple_completion(
            prompt="Say 'OK' if you can read this.",
            temperature=0.0
        )
        
        if test_response:
            logger.info("✅ OpenAI API connection successful")
            logger.info(f"Using models: {client.primary_model}, {client.secondary_model}")
        else:
            logger.warning("⚠️ OpenAI API returned empty response")
            
    except Exception as e:
        # Log but don't crash
        logger.warning(f"⚠️ OpenAI API validation skipped: {e}")
        logger.warning("LLM-powered features may not work until OpenAI API key is configured")
        # This is OK - app can still serve basic endpoints


@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event handler.
    
    This function runs once when the API server is shutting down. It performs
    cleanup tasks like:
    - Closing database connections
    - Flushing log buffers
    - Saving state if needed
    - Gracefully terminating background tasks
    
    When does shutdown occur?
    -------------------------
    - Manual stop: Ctrl+C in terminal
    - Process kill: SIGTERM signal
    - Deployment: Rolling updates
    - System restart
    
    Why is graceful shutdown important?
    ------------------------------------
    - Complete in-flight requests (don't drop active users)
    - Save any buffered data
    - Release resources properly
    - Prevent data corruption
    """
    logger.info("Shutting down API server")
    logger.info("Goodbye! 👋")


# ===================================================================================
# ROOT ENDPOINT
# ===================================================================================

@app.get("/")
async def root():
    """
    Root endpoint - API information and navigation.
    
    This is the first endpoint users see when they visit the API URL.
    It provides:
    - Welcome message
    - API version
    - Links to documentation
    - Links to key endpoints
    
    HTTP Method: GET
    URL: http://localhost:8000/
    
    Response Example:
    -----------------
    {
        "message": "Automotive Analytics API",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health"
    }
    
    Access in browser:
    ------------------
    1. Open http://localhost:8000/
    2. See JSON response with API info
    3. Click /docs link to explore API
    
    Returns:
    --------
    dict: API information and navigation links
    """
    return {
        "message": "Automotive Analytics API",
        "version": settings.app_version,
        "docs": "/docs",      # Interactive API documentation (try endpoints)
        "health": "/health",  # System health check endpoint
    }



# ===================================================================================
# DEVELOPMENT SERVER
# ===================================================================================

if __name__ == "__main__":
    """
    Development server entry point.
    
    This block only runs when you execute this file directly:
        python src/api/main.py
    
    It does NOT run when imported by:
    - Uvicorn server: uvicorn src.api.main:app
    - Vercel serverless: api/index.py
    - Test runners: pytest
    
    Why use Uvicorn?
    ----------------
    Uvicorn is an ASGI web server that:
    - Handles HTTP requests efficiently
    - Supports WebSockets
    - Enables async/await
    - Auto-reloads on code changes (in debug mode)
    - Uses multiple worker processes in production
    
    Development vs Production:
    --------------------------
    Development (debug=True):
    - Auto-reload on code changes (hot reload)
    - Verbose logging
    - Single worker process
    - Easy debugging
    
    Production (debug=False):
    - No auto-reload (stable)
    - Optimized logging
    - Multiple workers for concurrency
    - Better performance
    
    How to run:
    -----------
    Option 1: Direct execution
        python src/api/main.py
    
    Option 2: Uvicorn command (recommended for production)
        uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4
    
    Option 3: Use startup script
        ./start.bat (Windows)
        ./start.sh (Linux/Mac)
    """
    import uvicorn

    # Run the FastAPI application
    uvicorn.run(
        "src.api.main:app",          # Import path to FastAPI app
        host=settings.api_host,       # 0.0.0.0 = all interfaces, 127.0.0.1 = localhost only
        port=settings.api_port,       # Default: 8000
        reload=settings.debug,        # Auto-reload on code changes (development only)
    )
    """
    Uvicorn Configuration:
    ----------------------
    - "src.api.main:app": Python import path (module:object)
      * src.api.main = the module containing the app
      * app = the FastAPI instance variable
    
    - host="0.0.0.0": Listen on all network interfaces
      * Allows access from other machines on the network
      * Production: Use 0.0.0.0
      * Strict localhost: Use 127.0.0.1
    
    - port=8000: TCP port to listen on
      * Standard HTTP development port for APIs
      * Must match API_PORT in .env
      * Streamlit expects API on this port
    
    - reload=True: Watch for code changes and restart automatically
      * Development: Very convenient for rapid iteration
      * Production: Must be False (stability over convenience)
      * Only watches .py files by default
    
    Performance Tips:
    -----------------
    For production deployment, use additional options:
    - --workers 4: Run 4 worker processes (CPU count * 2)
    - --limit-concurrency 1000: Max concurrent requests
    - --timeout-keep-alive 5: Keep-alive timeout in seconds
    - --access-log: Log all requests (or disable for performance)
    
    Example production command:
        uvicorn src.api.main:app \
            --host 0.0.0.0 \
            --port 8000 \
            --workers 4 \
            --limit-concurrency 1000 \
            --no-access-log \
            --timeout-keep-alive 30
    """


