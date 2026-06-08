"""
Application configuration using Pydantic Settings.

Centralizes all app-level configuration so environment variables
or .env files can override defaults without touching code.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    APP_NAME: str = "AI Chat Application"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "Day 1 — FastAPI backend with clean layered architecture"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton instance — import this wherever config is needed
settings = Settings()
