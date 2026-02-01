"""
Vercel serverless function handler for FastAPI application
"""

from app.main import app

# Vercel supports ASGI apps directly, no need for Mangum
# Export the app directly - Vercel will handle the ASGI conversion
__all__ = ["app"]
