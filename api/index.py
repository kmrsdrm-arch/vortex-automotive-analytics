"""
Vercel serverless function entry point for FastAPI.
This file adapts the FastAPI application to work with Vercel's serverless platform.
"""

import sys
import os

# Add project root to Python path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the FastAPI application
from src.api.main import app

# Export for Vercel
# Vercel's Python runtime looks for 'app' or 'handler' variable
handler = app
