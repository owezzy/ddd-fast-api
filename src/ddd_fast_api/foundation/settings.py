"""Typed application settings for the foundation phase."""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from the environment or an optional .env file."""

    model_config = SettingsConfigDict(
        env_prefix="DDD_FAST_API_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "ddd-fast-api"
    app_env: Literal["development", "test", "production"] = "development"
    app_debug: bool = False
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    app_log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ddd_fast_api"
    catalog_repository_backend: Literal["memory", "sqlalchemy"] = "memory"
    identity_repository_backend: Literal["memory", "sqlalchemy"] = "memory"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the shared settings instance for application wiring."""

    return Settings()
