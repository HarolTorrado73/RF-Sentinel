"""API REST para RF Sentinel."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="RF Sentinel API",
    description="API para análisis de radiofrecuencia",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/health")
async def health_check() -> dict:
    return {"status": "healthy", "version": "0.1.0"}


@app.post("/scan", response_model=ScanResponse)
async def start_scan(request: ScanRequest) -> ScanResponse:
    if request.start_frequency >= request.stop_frequency:
        raise HTTPException(
            status_code=400, detail="start_frequency must be less than stop_frequency"
        )
    return ScanResponse(scan_id="scan_001", status="running", progress=0.0, signals_detected=0)


@app.get("/scan/{scan_id}", response_model=ScanResponse)
async def get_scan(scan_id: str) -> ScanResponse:
    return ScanResponse(scan_id=scan_id, status="completed", progress=100.0, signals_detected=5)


@app.post("/detect", response_model=list[SignalResponse])
async def detect_signals(capture_id: int = 1) -> list[SignalResponse]:
    _ = capture_id  # TODO: use for real implementation
    return [
        SignalResponse(
            id=1,
            frequency=433.92e6,
            bandwidth=100e3,
            power=-45.0,
            modulation="ASK",
            classification="Sensor",
            confidence=0.85,
        )
    ]


@app.post("/classify", response_model=SignalResponse)
async def classify_signal(frequency: float, bandwidth: float, power: float) -> SignalResponse:
    return SignalResponse(
        id=1,
        frequency=frequency,
        bandwidth=bandwidth,
        power=power,
        modulation="Unknown",
        classification="Unknown",
        confidence=0.0,
    )


@app.get("/capture", response_model=list[CaptureResponse])
async def get_captures(_limit: int = 100, _offset: int = 0) -> list[CaptureResponse]:
    return []


@app.get("/capture/{capture_id}", response_model=CaptureResponse)
async def get_capture(_capture_id: int) -> CaptureResponse:
    raise HTTPException(status_code=404, detail="Capture not found")


@app.post("/capture", response_model=CaptureResponse)
async def create_capture(frequency: float, _duration: float = 10.0) -> CaptureResponse:
    return CaptureResponse(
        id=1,
        timestamp="2024-01-01T00:00:00Z",
        center_frequency=frequency,
        sample_rate=10e6,
        signals=[],
    )


@app.post("/export/pdf")
async def export_pdf(capture_id: int) -> dict:
    return {"download_url": f"/downloads/capture_{capture_id}.pdf"}


@app.post("/export/json")
async def export_json(capture_id: int) -> dict:
    return {"download_url": f"/downloads/capture_{capture_id}.json"}
