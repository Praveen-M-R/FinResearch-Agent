"""
API v1 Pydantic schemas (request/response models)
"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health check response model"""

    status: str
    app: str
    version: str
    environment: str


class DetailedHealthResponse(HealthResponse):
    """Detailed health check response model"""

    debug: bool
