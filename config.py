import os
from pathlib import Path
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Core minor comment refresh
    APP_NAME: str = "Automation Center"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    SECRET_KEY: str = "dev-secret-key-change-in-prod"
    ENVIRONMENT: str = "development"  # development | testing | production

    # Database
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./dev.db",  # async SQLite for dev
        description="Async database URL (e.g., sqlite+aiosqlite:///, postgresql+asyncpg:///)"
    )

    # API
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"  # comma-separated

    # Logging
    LOG_LEVEL: str = "INFO"

    # Search
    SEARCH_MEMORY_LIMIT: int = 1000  # max tasks to load into memory for in-memory search

    # --- Derived & Validation ---
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"

    @property
    def is_testing(self) -> bool:
        return self.ENVIRONMENT == "testing"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.BACKEND_CORS_ORIGINS.split(",") if o.strip()]

    # Pydantic v2 config
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


# Load and validate settings once
try:
    settings = Settings()
except ValidationError as e:
    raise RuntimeError(f"Configuration error: {e}") from e

# Export for easy access
__all__ = ["settings"]