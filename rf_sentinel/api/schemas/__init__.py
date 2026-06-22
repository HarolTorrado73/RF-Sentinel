"""Schemas Pydantic para la API."""

from pydantic import BaseModel, Field


class ScanRequest(BaseModel):
    start_frequency: float = Field(..., gt=0, description="Frecuencia inicial en Hz")
    stop_frequency: float = Field(..., gt=0, description="Frecuencia final en Hz")
    step: float = Field(default=1e6, description="Paso de frecuencia en Hz")
    dwell_time: float = Field(default=0.1, description="Tiempo de estancia en cada frecuencia")
    sample_rate: float = Field(default=10e6, description="Tasa de muestreo en Hz")


class SignalResponse(BaseModel):
    id: int
    frequency: float
    bandwidth: float
    power: float
    modulation: str | None = None
    classification: str | None = None
    confidence: float | None = None


class CaptureResponse(BaseModel):
    id: int
    timestamp: str
    center_frequency: float
    sample_rate: float
    peak_power: float | None = None
    noise_floor: float | None = None
    signals: list[SignalResponse] = []


class ScanResponse(BaseModel):
    scan_id: str
    status: str
    progress: float
    signals_detected: int = 0
