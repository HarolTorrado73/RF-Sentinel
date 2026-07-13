from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.schemas.scan import Scan, ScanCreate
from app.schemas.user import User
from app.services.scan import ScanService

router = APIRouter()


@router.get("/", response_model=list[Scan])
async def read_scans(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    scans = await ScanService.get_multi(db)
    return scans


@router.post("/", response_model=Scan)
async def create_scan(
    scan_in: ScanCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    scan = await ScanService.create(db, scan_in, current_user.id)
    return scan


@router.get("/{scan_id}", response_model=Scan)
async def read_scan(
    scan_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    scan = await ScanService.get(db, scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan


@router.post("/{scan_id}/execute")
async def execute_scan(
    scan_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    scan = await ScanService.execute(db, scan_id)
    return scan