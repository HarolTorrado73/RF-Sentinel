"""Sesiones y engines de base de datos."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from rf_sentinel.core.config import settings

SYNC_DATABASE_URL = settings.SYNC_DATABASE_URL

_sync_engine = None
_sync_session_local = None


def _get_sync_engine():
    global _sync_engine
    if _sync_engine is None:
        _sync_engine = create_engine(SYNC_DATABASE_URL, echo=False)
    return _sync_engine


def _get_sync_session_local():
    global _sync_session_local
    if _sync_session_local is None:
        try:
            from sqlalchemy.orm import Session  # noqa: F401

            _sync_session_local = sessionmaker(
                _get_sync_engine(), class_=Session, expire_on_commit=False
            )
        except ImportError:
            pass
    return _sync_session_local


def get_db():  # type: ignore[return]
    """Obtiene sesión de base de datos sync (legacy)."""
    session_local = _get_sync_session_local()
    if session_local is None:
        raise RuntimeError("SQLAlchemy Session no disponible")
    with session_local() as session:
        yield session


def init_db() -> None:
    """Inicializa la base de datos."""
    from rf_sentinel.database.models.capture import Base as CaptureBase
    from rf_sentinel.database.models.signal import Base as SignalBase

    sync_engine = _get_sync_engine()
    CaptureBase.metadata.create_all(sync_engine)
    SignalBase.metadata.create_all(sync_engine)
