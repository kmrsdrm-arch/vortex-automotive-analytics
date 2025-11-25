"""
Vercel Serverless Function Entry Point
"""

from fastapi import FastAPI

# Create a minimal FastAPI app
app = FastAPI(title="Vortex API")

@app.get("/")
def root():
    return {
        "message": "Vortex API - Minimal Version Working!",
        "status": "ok",
        "version": "debug"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

# Vercel handler
handler = app
