from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.session import Session, SessionCreate, SessionUpdate
from app.services.session import SessionService
from app.api.deps import get_db, get_current_user

router = APIRouter()


@router.get("/", response_model=list[Session])
async def list_sessions(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    sessions = await SessionService.get_multi(db)
    return sessions


@router.get("/{session_id}", response_model=Session)
async def get_session(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    session = await SessionService.get(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.post("/", response_model=Session)
async def create_session(
    session_in: SessionCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    session = await SessionService.create(db, session_in)
    return session


@router.put("/{session_id}", response_model=Session)
async def update_session(
    session_id: int,
    session_in: SessionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    session = await SessionService.update(db, session_id, session_in)
    return session


@router.delete("/{session_id}")
async def delete_session(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    await SessionService.delete(db, session_id)
    return {"message": "Session deleted"}