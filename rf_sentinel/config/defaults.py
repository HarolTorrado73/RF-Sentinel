"""Valores por defecto de configuración."""

DEFAULT_DATABASE_URL = "sqlite+aiosqlite:///rf_sentinel.db"
DEFAULT_SYNC_DATABASE_URL = "sqlite:///rf_sentinel.db"
DEFAULT_API_HOST = "0.0.0.0"
DEFAULT_API_PORT = 8000
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_SDR_DEVICE = "mock"
DEFAULT_CORS_ORIGINS: list[str] = []
DEFAULT_ENABLE_PLUGINS = True
