"""Tipos compartidos entre módulos."""

from datetime import datetime
from typing import TypedDict


class SignalDict(TypedDict):
    """Diccionario de señal detectada."""
    frequency: float
    bandwidth: float
    power: float
    modulation: str | None
    classification: str | None
    confidence: float | None
    timestamp: datetime


class CaptureDict(TypedDict):
    """Diccionario de captura."""
    id: int
    timestamp: datetime
    center_frequency: float
    sample_rate: float
    bandwidth: float | None
    duration: float
    filename: str | None
    peak_power: float | None
    noise_floor: float | None
    signals: list[SignalDict]


class ScanDict(TypedDict):
    """Diccionario de escaneo."""
    scan_id: str
    status: str
    progress: float
    start_freq: float
    stop_freq: float
    step: float
    signals_detected: int
