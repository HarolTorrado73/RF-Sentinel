"""Core: tipos, eventos, configuración y excepciones compartidas."""

from rf_sentinel.core.config import Settings, settings
from rf_sentinel.core.events import (
    EVENT_SCAN_STARTED,
    EVENT_SCAN_STOPPED,
    EventBus,
)
from rf_sentinel.core.exceptions import (
    CaptureError,
    ClassificationError,
    DeviceError,
    RFSError,
    ScanError,
)
from rf_sentinel.core.types import CaptureDict, ScanDict, SignalDict

__all__ = [
    "Settings",
    "settings",
    "EventBus",
    "EVENT_SCAN_STARTED",
    "EVENT_SCAN_STOPPED",
    "SignalDict",
    "CaptureDict",
    "ScanDict",
    "RFSError",
    "DeviceError",
    "ScanError",
    "CaptureError",
    "ClassificationError",
]
