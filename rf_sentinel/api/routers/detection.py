"""Router de detección."""

import numpy as np
from fastapi import APIRouter, Depends

from rf_sentinel.api.dependencies import get_detector
from rf_sentinel.api.schemas import SignalResponse
from rf_sentinel.detection.energy import EnergyDetector

router = APIRouter(prefix="/detect", tags=["detection"])


@router.post("", response_model=list[SignalResponse])
async def detect_signals(
    capture_id: int = 1,
    detector: EnergyDetector = Depends(get_detector),  # noqa: B008
) -> list[SignalResponse]:
    _ = capture_id
    samples = np.random.randn(4096).astype(np.complex64)
    detections = detector.detect(samples)
    return [
        SignalResponse(
            id=i + 1,
            frequency=d.get("frequency", 0.0),
            bandwidth=d.get("bandwidth", 0.0),
            power=d.get("power", 0.0),
            modulation="ASK",
            classification="Sensor",
            confidence=0.85,
        )
        for i, d in enumerate(detections)
    ]
