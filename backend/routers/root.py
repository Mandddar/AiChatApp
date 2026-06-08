"""
Root router — the application landing endpoint.
"""

from fastapi import APIRouter

from core.config import settings

router = APIRouter(tags=["Root"])


@router.get(
    "/",
    summary="Root endpoint",
    description="Returns a welcome message with basic application info.",
)
async def root() -> dict:
    """Application entry point — confirms the API is reachable."""

    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }
