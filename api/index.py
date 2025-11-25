"""
Vercel serverless function entry point for FastAPI.
This file adapts the FastAPI application to work with Vercel's serverless platform.
"""

import sys
import os

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import FastAPI app
from src.api.main import app

# Vercel expects an 'app' or 'handler' export
# This makes the FastAPI app available to Vercel
handler = app
