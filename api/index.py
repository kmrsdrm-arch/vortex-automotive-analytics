"""
===================================================================================
Vercel Serverless Function Entry Point
===================================================================================

This file adapts our FastAPI application to run on Vercel's serverless platform.

What is Vercel?
---------------
Vercel is a cloud platform for deploying web applications. It uses a
"serverless" architecture where:
- No always-running servers
- Functions spin up on-demand when requests arrive
- Auto-scales from 0 to thousands of requests
- Pay only for actual usage (not idle time)

What is Serverless?
-------------------
Traditional servers:
- Always running 24/7
- Fixed capacity
- Pay for uptime even with no traffic
- Manual scaling needed

Serverless functions:
- Start only when request arrives (cold start)
- Automatic scaling
- Pay per request
- Zero maintenance

How Vercel Python Runtime Works:
---------------------------------
1. User makes HTTP request to your Vercel URL
2. Vercel routes request to appropriate serverless function
3. Vercel looks for this file (api/index.py)
4. Imports and executes this file
5. Looks for 'app' or 'handler' variable
6. Passes HTTP request to FastAPI app
7. FastAPI processes request and returns response
8. Vercel sends response back to user
9. Function may stay warm for a few minutes or shutdown

Why This Adapter File?
----------------------
Our main application is in src/api/main.py, but Vercel expects a specific
structure:
- Entry file must be in api/ folder
- Must export 'app' or 'handler' variable
- Must handle Python import paths

This file bridges the gap between Vercel's expectations and our app structure.

File Structure:
---------------
Project Root/
├── api/
│   └── index.py ← YOU ARE HERE (Vercel entry point)
├── src/
│   ├── api/
│   │   └── main.py ← Actual FastAPI app
│   ├── database/
│   ├── llm/
│   └── ...
├── config/
├── requirements.txt
└── vercel.json ← Vercel configuration

Deployment:
-----------
1. Push code to GitHub
2. Connect GitHub repo to Vercel
3. Vercel automatically:
   - Detects Python project
   - Installs dependencies from requirements.txt
   - Builds serverless functions from api/ folder
   - Deploys to global CDN
4. Your API is live at: https://your-project.vercel.app

Limitations:
------------
- Cold starts: First request after idle period is slower (1-3 seconds)
- Execution time: Max 10 seconds per request (Hobby plan)
- Memory: Max 1GB (Hobby plan)
- Not suitable for: Long-running tasks, WebSockets, stateful operations

Best For:
---------
✅ REST APIs with quick responses
✅ Microservices
✅ Prototypes and MVPs
✅ Low to medium traffic applications
✅ Auto-scaling requirements

Author: Automotive Analytics Team
Version: 2.0.0
===================================================================================
"""

import sys
import os


# ===================================================================================
# PYTHON PATH CONFIGURATION
# ===================================================================================

# Get the absolute path to project root (one level up from api/ folder)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
"""
Why modify sys.path?
--------------------
When Vercel runs this file, Python doesn't know about our src/ folder structure.
We need to add the project root to Python's import search path so it can find:
- src.api.main
- config.settings
- config.database
- etc.

How it works:
-------------
1. __file__ = absolute path to this file (api/index.py)
2. os.path.dirname(__file__) = parent directory (api/)
3. join(..., '..') = go up one level (project root)
4. os.path.abspath = convert to absolute path
5. sys.path.insert(0, ...) = add to front of import search path

Example paths:
--------------
- __file__: /var/task/api/index.py
- dirname: /var/task/api
- join ..: /var/task/api/..
- abspath: /var/task
- sys.path: ['/var/task', ...]

Now Python can import: from src.api.main import app
"""

# Check if project root is already in sys.path (avoid duplicates)
if project_root not in sys.path:
    # Insert at position 0 (front of list) so it's checked first
    sys.path.insert(0, project_root)
    """
    Why insert at position 0?
    -------------------------
    Python searches sys.path in order. By inserting at the front, we ensure
    our project modules are found first, before any system modules with
    similar names.
    
    If we used append():
    - Our modules might conflict with system modules
    - Harder to debug import issues
    - Unpredictable behavior
    
    With insert(0):
    - Our modules always take precedence
    - Clear, predictable import resolution
    - Easy to debug
    """


# ===================================================================================
# IMPORT FASTAPI APPLICATION
# ===================================================================================

# Import the main FastAPI application from src/api/main.py
from src.api.main import app
"""
This import brings in the complete FastAPI application with:
- All route handlers (analytics, insights, reports, etc.)
- Middleware (CORS, logging)
- Configuration (settings, database)
- Dependencies (database sessions)
- Lifecycle events (startup, shutdown)

The 'app' variable is the FastAPI() instance created in src/api/main.py.
"""


# ===================================================================================
# VERCEL HANDLER EXPORT
# ===================================================================================

# Vercel's Python runtime looks for 'app' or 'handler' variable in this file
handler = app
"""
Export FastAPI app as 'handler' for Vercel.

Why 'handler'?
--------------
Vercel's Python runtime expects a callable named 'handler' that can process
HTTP requests. FastAPI applications are ASGI applications, which Vercel's
runtime can automatically wrap and execute.

Alternative names:
------------------
Vercel also accepts:
- app = app (if you want to keep the name 'app')
- handler = app (more explicit for serverless)

Both work the same way.

What happens at runtime:
------------------------
1. Vercel receives HTTP request
2. Loads this file (api/index.py)
3. Finds 'handler' variable
4. Checks that it's an ASGI application (FastAPI is)
5. Wraps it with ASGI adapter
6. Passes request to FastAPI
7. Returns response

Request Flow:
-------------
Client → Vercel CDN → Serverless Function → handler (this variable)
       ↓
FastAPI app → Middleware → Routes → Database → Response
       ↓
Client ← Vercel CDN ← Serverless Function ← FastAPI Response

Environment Variables:
----------------------
Vercel automatically provides environment variables from:
1. Vercel Dashboard (Settings → Environment Variables)
2. .env file (if using vercel dev locally)
3. vercel.json env section

These are loaded by config/settings.py via python-dotenv.

Local Testing:
--------------
You can test this Vercel setup locally with:
```bash
vercel dev
```

This starts a local server that simulates Vercel's serverless environment.

Production Deployment:
----------------------
```bash
vercel --prod
```

Or connect your GitHub repo to Vercel for automatic deployments on push.

Monitoring:
-----------
View logs and analytics in Vercel Dashboard:
- https://vercel.com/dashboard
- Real-time logs
- Error tracking
- Performance metrics
- Usage statistics

Cold Starts:
------------
If no requests for several minutes, function "goes cold" and needs to restart:
- Cold start time: 1-3 seconds
- Warm start time: <100ms

To minimize cold starts:
- Use Vercel Pro (keeps functions warm longer)
- Implement health check pings
- Use background jobs for warmup
- Optimize dependencies (fewer imports = faster startup)

Debugging:
----------
If deployment fails:
1. Check Vercel build logs
2. Verify requirements.txt has all dependencies
3. Ensure vercel.json configuration is correct
4. Test locally with 'vercel dev'
5. Check environment variables are set

Common Issues:
--------------
❌ Import errors: Check sys.path modification above
❌ Module not found: Missing dependency in requirements.txt
❌ Timeout: Endpoint takes > 10 seconds (Hobby plan limit)
❌ Memory error: Endpoint uses > 1GB RAM (Hobby plan limit)

Best Practices:
---------------
✅ Keep endpoint responses < 1 second
✅ Use async/await for I/O operations
✅ Minimize cold start time (lazy imports, optimize dependencies)
✅ Handle errors gracefully (don't let function crash)
✅ Log important events (viewable in Vercel dashboard)
✅ Set appropriate timeout limits
✅ Cache expensive computations
"""

import sys
import os

# ===================================================================================
# PYTHON PATH CONFIGURATION
# ===================================================================================

# Get the absolute path to project root (one level up from api/ folder)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add project root to Python's import search path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# ===================================================================================
# IMPORT FASTAPI APPLICATION
# ===================================================================================

try:
    # Try to import the main FastAPI application
    from src.api.main import app
    handler = app
    
except Exception as e:
    # If import fails, create a simple FastAPI app that shows the error
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    import traceback
    
    app = FastAPI(title="Vortex API - Error Debug")
    
    @app.get("/")
    async def root():
        return JSONResponse({
            "error": "Failed to import main application",
            "message": str(e),
            "traceback": traceback.format_exc(),
            "python_version": sys.version,
            "sys_path": sys.path[:5]  # Show first 5 paths
        }, status_code=500)
    
    @app.get("/health")
    async def health():
        return JSONResponse({
            "status": "error",
            "error": str(e)
        }, status_code=500)
    
    handler = app
