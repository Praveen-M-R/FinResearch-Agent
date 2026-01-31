"""
API v1 router - aggregates all v1 endpoints
"""

from fastapi import APIRouter

from app.api.v1 import health

api_router = APIRouter()

# Include health check router
api_router.include_router(health.router, tags=["Health"])
