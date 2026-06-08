"""
Health-check router.

Provides a lightweight endpoint for load balancers, orchestration
systems, or monitoring dashboards to verify the service is alive.
"""

from datetime import datetime, timezone

from fastapi import APIRouter

from core.config import settings

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    summary="Health check",
    description="Returns current service health status and uptime metadata.",
)
async def health_check() -> dict:
    """Lightweight liveness probe — always returns status ok."""

    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
