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
    APP_DESCRIPTION: str = "Day 2 — FastAPI backend with clean layered architecture"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost/ai_chat_app"

    # AI Model
    GEMINI_API_KEY: str | None = None

    # JWT Authentication
    SECRET_KEY: str = "a_very_secret_key_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton instance — import this wherever config is needed
settings = Settings()
