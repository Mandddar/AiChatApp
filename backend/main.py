"""
AI Chat Application — FastAPI Entry Point

This module bootstraps the FastAPI application, configures metadata
for the auto-generated Swagger UI, and registers all routers.

Run with:
    uvicorn main:app --reload
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from database.session import engine
from database.base import Base
from routers import root, health, auth, users, chats, documents

# Import all models so Base.metadata.create_all can discover them
import models.user      # noqa: F401
import models.chat      # noqa: F401
import models.message   # noqa: F401
import models.document  # noqa: F401


# ---------------------------------------------------------------------------
# Lifespan (replaces deprecated on_event)
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    print(f"\n>>> {settings.APP_NAME} v{settings.APP_VERSION} is running!")
    print(f"    Swagger UI  -> http://localhost:8000/docs")
    print(f"    ReDoc       -> http://localhost:8000/redoc\n")
    yield
    # Shutdown
    print("\n>>> Shutting down gracefully...\n")


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Router registration
# ---------------------------------------------------------------------------

app.include_router(root.router)       # GET /
app.include_router(health.router)     # GET /health
app.include_router(auth.router)       # /auth register/login
app.include_router(users.router)      # /users endpoints
app.include_router(chats.router)      # /chats endpoints
app.include_router(documents.router)  # /documents endpoints
