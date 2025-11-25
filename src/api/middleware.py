"""Custom middleware for FastAPI."""

import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.utils.logger import get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging requests."""

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log request
        logger.info(f"Request: {request.method} {request.url.path}")

        # Process request
        response = await call_next(request)

        # Log response
        process_time = time.time() - start_time
        logger.info(
            f"Response: {response.status_code} - {request.method} {request.url.path} - {process_time:.3f}s"
        )

        # Add custom header
        response.headers["X-Process-Time"] = str(process_time)

        return response

