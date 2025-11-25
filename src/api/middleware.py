"""
===================================================================================
Custom Middleware for FastAPI
===================================================================================

Middleware intercepts and processes ALL requests and responses passing through
the API. Think of it as a "filter" that can:
- Log requests and responses
- Measure performance
- Add custom headers
- Handle errors globally
- Implement authentication
- Rate limiting
- CORS handling

What is Middleware?
-------------------
Middleware sits between the client and your endpoint handlers. It's like
a checkpoint that every request must pass through.

Request Flow:
-------------
1. Client sends request
2. → Middleware #1 (CORS)
3. → Middleware #2 (Logging) ← This file
4. → Middleware #3 (Authentication)
5. → Your endpoint handler
6. ← Response back through middleware (reverse order)
7. ← Client receives response

Why Use Middleware?
-------------------
✅ DRY Principle: Write once, applies to all endpoints
✅ Separation of Concerns: Keep cross-cutting logic separate
✅ Consistent Behavior: Same logging/timing for all requests
✅ Easy to Add/Remove: No endpoint code changes needed

Common Middleware Uses:
-----------------------
- Request/response logging (this file)
- Performance monitoring
- Error handling
- Authentication/authorization
- Request ID tracking
- Compression
- Caching
- Rate limiting

Author: Automotive Analytics Team
Version: 2.0.0
===================================================================================
"""

import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.utils.logger import get_logger

logger = get_logger(__name__)


# ===================================================================================
# LOGGING MIDDLEWARE
# ===================================================================================

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging and timing all API requests.
    
    This middleware:
    1. Logs every incoming request (method and path)
    2. Measures processing time
    3. Logs response status and duration
    4. Adds X-Process-Time header to responses
    
    What is BaseHTTPMiddleware?
    ----------------------------
    It's a base class provided by Starlette (FastAPI's foundation) that makes
    it easy to create custom middleware. You only need to implement the
    `dispatch` method, which receives:
    - request: The incoming HTTP request
    - call_next: A function to call the next middleware or endpoint
    
    How It Works:
    -------------
    1. Request arrives from client
    2. dispatch() method is called
    3. We log the request and start timer
    4. We call call_next() to pass to next middleware/endpoint
    5. call_next() returns the response
    6. We log response and stop timer
    7. We add custom headers to response
    8. Response is sent back to client
    
    Example Log Output:
    -------------------
    Request: GET /api/analytics/sales
    Response: 200 - GET /api/analytics/sales - 0.234s
    
    Request: POST /api/query/natural-language
    Response: 200 - POST /api/query/natural-language - 1.567s
    
    Request: GET /api/insights/generate
    Response: 500 - GET /api/insights/generate - 0.089s
    
    Benefits:
    ---------
    ✅ Performance monitoring: See which endpoints are slow
    ✅ Debugging: Track request flow in logs
    ✅ Usage analytics: Count requests per endpoint
    ✅ Error detection: Spot failing endpoints quickly
    ✅ Client timing: X-Process-Time header for frontend monitoring
    """

    async def dispatch(self, request: Request, call_next):
        """
        Process each request and response.
        
        This method is called for EVERY request that comes to the API.
        It runs before and after the endpoint handler.
        
        Execution Flow:
        ---------------
        1. Record start time
        2. Log incoming request details
        3. Pass request to next middleware/endpoint (await call_next)
        4. Wait for response to come back
        5. Calculate elapsed time
        6. Log response details
        7. Add performance header
        8. Return response to client
        
        The 'await' Keyword:
        --------------------
        `await call_next(request)` means:
        - Pause this function
        - Let the endpoint process the request
        - Resume when endpoint returns response
        - This is async/await in Python (non-blocking I/O)
        
        Parameters:
        -----------
        request : Request
            The incoming HTTP request object containing:
            - method: HTTP verb (GET, POST, PUT, DELETE, etc.)
            - url: Full URL including path and query parameters
            - headers: Request headers (Authorization, Content-Type, etc.)
            - body: Request body (for POST/PUT requests)
            - client: Client IP address and port
        
        call_next : Callable
            Function to call the next middleware or endpoint.
            Returns the response after processing.
        
        Returns:
        --------
        Response
            The HTTP response object with added headers:
            - X-Process-Time: Time taken to process request (in seconds)
            - All original response headers and body
        
        Example Request/Response Cycle:
        --------------------------------
        >>> # Client sends: GET /api/analytics/sales?start_date=2024-01-01
        >>> # Middleware logs: "Request: GET /api/analytics/sales"
        >>> # Endpoint processes for 0.234 seconds
        >>> # Middleware logs: "Response: 200 - GET /api/analytics/sales - 0.234s"
        >>> # Client receives response with header: X-Process-Time: 0.234
        
        Performance Considerations:
        ---------------------------
        - time.time() is very fast (<1 microsecond)
        - Logging is buffered (minimal performance impact)
        - No synchronous I/O blocks (all async)
        - Adds <1ms overhead per request
        
        Security Note:
        --------------
        This middleware logs request paths, which might contain sensitive data
        in query parameters (e.g., /api/user?email=test@example.com).
        
        In production, consider:
        - Filtering sensitive query params before logging
        - Using structured logging with parameter masking
        - Separating access logs from application logs
        """
        
        # ===============================================================================
        # STEP 1: Record start time for performance measurement
        # ===============================================================================
        start_time = time.time()
        """
        time.time() returns current time in seconds since Unix epoch (Jan 1, 1970).
        Example: 1732545845.234 (Nov 25, 2024, 14:30:45.234)
        
        We'll subtract this from end time to get elapsed seconds.
        """

        # ===============================================================================
        # STEP 2: Log the incoming request
        # ===============================================================================
        logger.info(f"Request: {request.method} {request.url.path}")
        """
        Log format: "Request: GET /api/analytics/sales"
        
        Components:
        - request.method: HTTP verb (GET, POST, PUT, DELETE, PATCH, OPTIONS)
        - request.url.path: URL path without query parameters
          * With query: /api/users?name=john → Logs: /api/users
          * To include query: use request.url instead of request.url.path
        
        Why log method and path?
        - Identify which endpoint was called
        - Track API usage patterns
        - Debug routing issues
        - Monitor endpoint popularity
        
        Additional info you could log:
        - request.client.host: Client IP address
        - request.headers.get("user-agent"): Browser/client info
        - request.url.query: Query parameters
        - request.headers.get("authorization"): Auth token (mask it!)
        """

        # ===============================================================================
        # STEP 3: Pass request to next middleware or endpoint
        # ===============================================================================
        response = await call_next(request)
        """
        call_next(request) does:
        1. Passes request to next middleware in chain (if any)
        2. Or passes to endpoint handler (if last middleware)
        3. Waits for response
        4. Returns response back to us
        
        The 'await' keyword means:
        - This function pauses here
        - Other requests can be processed concurrently
        - Resumes when response is ready
        - This is how async/await achieves high performance
        
        During this await:
        - Database queries run
        - External API calls happen
        - LLM completions are generated
        - Business logic executes
        
        When it returns:
        - response contains status code (200, 404, 500, etc.)
        - response contains headers (Content-Type, etc.)
        - response contains body (JSON, HTML, etc.)
        """

        # ===============================================================================
        # STEP 4: Calculate processing time
        # ===============================================================================
        process_time = time.time() - start_time
        """
        Calculate elapsed time in seconds.
        
        Example:
        - start_time: 1732545845.234
        - end_time:   1732545845.468
        - process_time: 0.234 seconds (234 milliseconds)
        
        Typical processing times:
        - Simple queries: 0.010-0.050s (10-50ms)
        - Complex analytics: 0.100-0.500s (100-500ms)
        - LLM calls: 1.000-5.000s (1-5 seconds)
        - Very slow (investigate!): >10s
        """

        # ===============================================================================
        # STEP 5: Log the response
        # ===============================================================================
        logger.info(
            f"Response: {response.status_code} - {request.method} {request.url.path} - {process_time:.3f}s"
        )
        """
        Log format: "Response: 200 - GET /api/analytics/sales - 0.234s"
        
        Components:
        - response.status_code: HTTP status code
          * 2xx: Success (200 OK, 201 Created, 204 No Content)
          * 3xx: Redirect (301 Moved, 302 Found, 304 Not Modified)
          * 4xx: Client error (400 Bad Request, 404 Not Found, 403 Forbidden)
          * 5xx: Server error (500 Internal Error, 503 Service Unavailable)
        
        - request.method: Same as request log (for correlation)
        - request.url.path: Same as request log (for correlation)
        - process_time:.3f: Time in seconds with 3 decimal places (milliseconds)
          * .3f formats: 0.234000 → "0.234"
        
        Why log response?
        - Monitor success rate (2xx vs 4xx vs 5xx)
        - Identify slow endpoints
        - Correlate with request (same line in logs)
        - Debug timing issues
        
        Pro tip: Use structured logging in production
        Instead of string formatting, use JSON:
        logger.info("request_processed", extra={
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "duration_ms": process_time * 1000
        })
        This makes logs easily searchable and parseable.
        """

        # ===============================================================================
        # STEP 6: Add custom header with processing time
        # ===============================================================================
        response.headers["X-Process-Time"] = str(process_time)
        """
        Add custom HTTP response header with processing time.
        
        Header name: X-Process-Time
        Header value: "0.234" (seconds as string)
        
        Why add this header?
        - Frontend can track API performance
        - Debugging: See if slowness is backend or network
        - Monitoring: Log on client side for real user monitoring
        - Developer experience: See timing in browser DevTools
        
        Client-side usage (JavaScript):
        const response = await fetch('/api/analytics/sales');
        const processTime = response.headers.get('X-Process-Time');
        console.log(`API took ${processTime}s`);
        
        Headers starting with "X-" are custom (non-standard):
        - X-Process-Time (this header)
        - X-Request-ID (for request tracking)
        - X-Rate-Limit-Remaining (for rate limiting)
        
        Standard headers don't use X- prefix:
        - Content-Type
        - Authorization
        - Cache-Control
        """

        # ===============================================================================
        # STEP 7: Return response to client
        # ===============================================================================
        return response
        """
        Return the response to previous middleware (or client if we're last).
        
        Response flow (reverse order of request):
        1. Our middleware returns response
        2. → Previous middleware processes it
        3. → CORS middleware adds CORS headers
        4. → FastAPI serializes to JSON/HTML
        5. → Uvicorn sends over HTTP
        6. → Client receives response
        
        The response object contains:
        - status_code: 200, 404, 500, etc.
        - headers: Dict of header name → value
        - body: JSON, HTML, or binary data
        - cookies: Set-Cookie headers
        
        After this return:
        - No more code in this function executes
        - Response is sent to client
        - Connection may be kept alive (HTTP keep-alive)
        - Next request can be processed
        """

