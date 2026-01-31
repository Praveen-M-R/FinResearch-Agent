"""
Main FastAPI application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from app.core.config import settings
from app.api.v1.router import api_router


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application

    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="AI-powered financial research and intelligence agent",
        debug=settings.DEBUG,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
    )

    # Configure CORS for development
    if settings.DEBUG:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Include API v1 router
    app.include_router(api_router, prefix="/api/v1")

    # Mount static files for UI
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # Redirect root to UI
    @app.get("/")
    async def root():
        """Redirect to chat UI"""
        return RedirectResponse(url="/static/index.html")

    return app


# Create application instance
app = create_application()
