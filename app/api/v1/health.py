"""
Health check endpoints
"""

from fastapi import APIRouter

from app.core.config import settings
from app.api.v1.types import HealthResponse, DetailedHealthResponse

router = APIRouter()


@router.get("/", response_model=HealthResponse, tags=["Health"])
async def root() -> HealthResponse:
    """
    Root endpoint - basic health check

    Returns:
        Basic health status information
    """
    return HealthResponse(
        status="healthy",
        app=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.APP_ENVIRONMENT,
    )


@router.get("/health", response_model=DetailedHealthResponse, tags=["Health"])
async def health_check() -> DetailedHealthResponse:
    """
    Detailed health check endpoint

    Returns:
        Detailed health status with debug information
    """
    return DetailedHealthResponse(
        status="healthy",
        app=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.APP_ENVIRONMENT,
        debug=settings.DEBUG,
    )
