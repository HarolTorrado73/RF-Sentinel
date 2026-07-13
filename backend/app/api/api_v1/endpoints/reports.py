from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.report import ReportService
from app.schemas.report import ReportCreate, Report
from app.api.deps import get_current_active_user, get_current_admin_user, get_db

router = APIRouter()


@router.post("/", response_model=Report)
async def create_report(
    report_in: ReportCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    report = await ReportService.create(db, report_in, current_user.id)
    return report


@router.get("/", response_model=list[Report])
async def get_reports(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    reports = await ReportService.get_multi(db)
    return reports


@router.get("/{report_id}", response_model=Report)
async def get_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    report = await ReportService.get(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.post("/{report_id}/generate")
async def generate_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    report = await ReportService.get(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    result = await ReportService.generate_report(db, report)
    report.file_path = result.get("file_path", "")
    await db.commit()

    return {"status": "generated", "file_path": report.file_path}


@router.get("/{report_id}/download")
async def download_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    report = await ReportService.get(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if not report.file_path or not Path(report.file_path).exists():
        raise HTTPException(status_code=404, detail="Report file not found")

    return FileResponse(
        path=report.file_path,
        filename=Path(report.file_path).name,
        media_type="application/octet-stream",
    )


@router.delete("/{report_id}")
async def delete_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_admin_user),
):
    await ReportService.delete(db, report_id)
    return {"message": "Report deleted"}