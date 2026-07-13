from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.schemas.target import Target, TargetCreate, TargetUpdate
from app.schemas.user import User
from app.services.target import TargetService

router = APIRouter()


@router.get("/", response_model=list[Target])
async def read_targets(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    targets = await TargetService.get_multi(db)
    return targets


@router.post("/", response_model=Target)
async def create_target(
    target_in: TargetCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    target = await TargetService.create(db, target_in, current_user.id)
    return target


@router.get("/{target_id}", response_model=Target)
async def read_target(
    target_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    target = await TargetService.get(db, target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    return target


@router.put("/{target_id}", response_model=Target)
async def update_target(
    target_id: int,
    target_in: TargetUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    target = await TargetService.update(db, target_id, target_in)
    return target


@router.delete("/{target_id}")
async def delete_target(
    target_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    await TargetService.delete(db, target_id)
    return {"message": "Target deleted"}