"""Repositorios de base de datos."""

from rf_sentinel.database.repositories.capture_repo import CaptureRepository
from rf_sentinel.database.repositories.signal_repo import SignalRepository

__all__ = ["CaptureRepository", "SignalRepository"]
