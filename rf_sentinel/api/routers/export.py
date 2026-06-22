"""Router de exportación."""

from fastapi import APIRouter, Depends

from rf_sentinel.api.dependencies import get_export_service
from rf_sentinel.services.export_service import ExportService

router = APIRouter(prefix="/export", tags=["export"])


@router.post("/pdf")
async def export_pdf(
    capture_id: int,
    export_service: ExportService = Depends(get_export_service),  # noqa: B008
) -> dict:
    _ = export_service
    return {"download_url": f"/downloads/capture_{capture_id}.pdf"}


@router.post("/json")
async def export_json(
    capture_id: int,
    export_service: ExportService = Depends(get_export_service),  # noqa: B008
) -> dict:
    _ = export_service
    return {"download_url": f"/downloads/capture_{capture_id}.json"}
