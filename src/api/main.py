"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings
from config.logging_config import logger
from src.api.middleware import LoggingMiddleware
from src.api.routes import health, analytics, insights, reports, query, data

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Automotive Analytics Pipeline with LLM-powered insights",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(health.router)
app.include_router(analytics.router)
app.include_router(insights.router)
app.include_router(reports.router)
app.include_router(query.router)
app.include_router(data.router)


@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"API server starting on {settings.api_host}:{settings.api_port}")
    
    # Validate OpenAI API connection
    try:
        from src.llm.core.client import client
        logger.info("Validating OpenAI API connection...")
        
        # Test with a simple completion
        test_response = client.simple_completion(
            "Say 'OK' if you can read this.",
            temperature=0.0
        )
        
        if test_response:
            logger.info("✅ OpenAI API connection successful")
            logger.info(f"Using models: {client.primary_model}, {client.secondary_model}")
        else:
            logger.warning("⚠️ OpenAI API returned empty response")
    except Exception as e:
        logger.error(f"❌ OpenAI API validation failed: {e}")
        logger.error("⚠️ LLM-powered features (NL Query, Insights, Reports) will not work properly")
        logger.error("Please check your OPENAI_API_KEY in .env file and ensure your account has sufficient credits")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    logger.info("Shutting down API server")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Automotive Analytics API",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )

