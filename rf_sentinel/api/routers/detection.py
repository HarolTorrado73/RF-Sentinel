"""Router de detección."""

import numpy as np
from fastapi import APIRouter, Depends

from rf_sentinel.api.dependencies import get_detection_pipeline
from rf_sentinel.api.schemas import DetectionRequest, SignalResponse
from rf_sentinel.services.pipeline import DetectionPipeline

router = APIRouter(prefix="/detect", tags=["detection"])


@router.post("", response_model=list[SignalResponse])
async def detect_signals(
    request: DetectionRequest,
    pipeline: DetectionPipeline = Depends(get_detection_pipeline),  # noqa: B008
) -> list[SignalResponse]:
    _ = request.capture_id
    samples = np.random.randn(4096).astype(np.complex64)
    detections = pipeline.run(samples)
    return [
        SignalResponse(
            id=i + 1,
            frequency=float(d.get("frequency", 0.0)),
            bandwidth=float(d.get("bandwidth", 0.0)),
            power=float(d.get("power", 0.0)),
            modulation=d.get("modulation"),
            classification=d.get("classification"),
            confidence=float(d.get("confidence", 0.0)) if d.get("confidence") is not None else None,
        )
        for i, d in enumerate(detections)
    ]
