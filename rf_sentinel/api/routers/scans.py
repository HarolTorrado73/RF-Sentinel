"""Router de escaneos."""

from fastapi import APIRouter, Depends, HTTPException

from rf_sentinel.api.dependencies import get_scan_service
from rf_sentinel.api.schemas import ScanRequest, ScanResponse
from rf_sentinel.services.scan_service import ScanService

router = APIRouter(prefix="/scan", tags=["scans"])


@router.post("", response_model=ScanResponse)
async def start_scan(
    request: ScanRequest,
    scan_service: ScanService = Depends(get_scan_service),  # noqa: B008
) -> ScanResponse:
    if request.start_frequency >= request.stop_frequency:
        raise HTTPException(
            status_code=400, detail="start_frequency must be less than stop_frequency"
        )
    scan_id = await scan_service.start_scan(
        request.start_frequency, request.stop_frequency, request.step
    )
    status = await scan_service.get_status(scan_id)
    return ScanResponse(scan_id=scan_id, **status)


@router.get("/{scan_id}", response_model=ScanResponse)
async def get_scan(
    scan_id: str,
    scan_service: ScanService = Depends(get_scan_service),  # noqa: B008
) -> ScanResponse:
    status = await scan_service.get_status(scan_id)
    if status.get("status") == "not_found":
        raise HTTPException(status_code=404, detail="Scan not found")
    return ScanResponse(scan_id=scan_id, **status)
