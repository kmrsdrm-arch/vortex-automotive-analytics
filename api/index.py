"""
Vercel serverless function entry point for FastAPI.
This file adapts the FastAPI application to work with Vercel's serverless platform.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api.main import app

# Vercel serverless function handler
def handler(request, context):
    """Handle requests through the FastAPI app."""
    return app(request, context)

# For Vercel, export the app
application = app

