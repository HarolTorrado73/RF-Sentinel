"""Legacy: modelos de base de datos para RF Sentinel.

Este módulo existe por compatibilidad con código existente.
Los modelos ahora residen en rf_sentinel.database.models.*
"""

import contextlib

from rf_sentinel.database.models.capture import Capture
from rf_sentinel.database.models.signal import Signal

with contextlib.suppress(Exception):
    from rf_sentinel.database.session import get_db, init_db  # noqa: F401

__all__ = ["Capture", "Signal"]
