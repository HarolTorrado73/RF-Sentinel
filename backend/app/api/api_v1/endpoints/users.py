from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import User, UserUpdate
from app.services.user import UserService
from app.api.deps import get_current_user, get_current_admin_user, get_db

router = APIRouter()


@router.get("/me", response_model=User)
async def read_user_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.put("/me", response_model=User)
async def update_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user = await UserService.update(db, current_user.id, user_in)
    return user


@router.get("/", response_model=list[User])
async def list_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    users = await UserService.get_multi(db)
    return users


@router.get("/{user_id}", response_model=User)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    user = await UserService.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    user = await UserService.update(db, user_id, user_in)
    return user