"""Configuración centralizada de RF Sentinel."""

import os
from dataclasses import dataclass, field


@dataclass
class Settings:
    """Settings globales de la aplicación."""

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///rf_sentinel.db")
    SYNC_DATABASE_URL: str = os.getenv("SYNC_DATABASE_URL", "sqlite:///rf_sentinel.db")
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    SDR_DEFAULT_DEVICE: str = os.getenv("SDR_DEFAULT_DEVICE", "mock")
    CORS_ALLOW_ORIGINS: list[str] = field(default_factory=list)
    ENABLE_PLUGINS: bool = os.getenv("ENABLE_PLUGINS", "true").lower() != "false"


settings = Settings()
