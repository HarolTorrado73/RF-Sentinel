"""Router de capturas."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from rf_sentinel.api.dependencies import get_capture_service
from rf_sentinel.api.schemas import CaptureResponse
from rf_sentinel.services.capture_service import CaptureService

router = APIRouter(prefix="/capture", tags=["captures"])


def _capture_to_response(capture) -> CaptureResponse:
    return CaptureResponse(
        id=capture.id,
        timestamp=capture.timestamp.isoformat() if isinstance(capture.timestamp, datetime) else str(capture.timestamp),
        center_frequency=capture.center_frequency,
        sample_rate=capture.sample_rate,
        peak_power=capture.peak_power,
        noise_floor=capture.noise_floor,
        signals=[],
    )


@router.get("", response_model=list[CaptureResponse])
async def list_captures(
    _limit: int = 100,
    _offset: int = 0,
    capture_service: CaptureService = Depends(get_capture_service),  # noqa: B008
) -> list[CaptureResponse]:
    captures = await capture_service.list_captures(limit=_limit)
    return [_capture_to_response(c) for c in captures]


@router.get("/{capture_id}", response_model=CaptureResponse)
async def get_capture(
    capture_id: int,
    capture_service: CaptureService = Depends(get_capture_service),  # noqa: B008
) -> CaptureResponse:
    capture = await capture_service.get_capture(capture_id)
    if not capture:
        raise HTTPException(status_code=404, detail="Capture not found")
    return _capture_to_response(capture)


@router.post("", response_model=CaptureResponse)
async def create_capture(
    frequency: float,
    _duration: float = 10.0,
    capture_service: CaptureService = Depends(get_capture_service),  # noqa: B008
) -> CaptureResponse:
    capture = await capture_service.create_capture(frequency, _duration)
    return _capture_to_response(capture)
