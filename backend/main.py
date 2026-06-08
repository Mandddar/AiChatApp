"""
AI Chat Application — FastAPI Entry Point (Day 1)

This module bootstraps the FastAPI application, configures metadata
for the auto-generated Swagger UI, and registers all routers.

Run with:
    uvicorn main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from routers import root, health, items

# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Router registration
#
# Each feature module exposes its own APIRouter instance.
# Registering them here keeps main.py as a thin composition root.
# ---------------------------------------------------------------------------

app.include_router(root.router)       # GET /
app.include_router(health.router)     # GET /health
app.include_router(items.router)      # /items CRUD


# ---------------------------------------------------------------------------
# Startup / shutdown lifecycle events
# ---------------------------------------------------------------------------

@app.on_event("startup")
async def on_startup() -> None:
    """Log a banner so you know the server is alive."""
    print(f"\n>>> {settings.APP_NAME} v{settings.APP_VERSION} is running!")
    print(f"    Swagger UI  -> http://localhost:8000/docs")
    print(f"    ReDoc       -> http://localhost:8000/redoc\n")


@app.on_event("shutdown")
async def on_shutdown() -> None:
    """Clean-up hook — nothing to tear down yet."""
    print("\n>>> Shutting down gracefully...\n")
