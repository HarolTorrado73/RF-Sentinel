from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.core.security import create_access_token, create_refresh_token, revoke_token
from app.schemas.token import Token, TokenRefresh
from app.schemas.user import UserCreate, User
from app.services.user import UserService
from jose import jwt
from app.core.config import settings

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await UserService.authenticate(
        db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    return Token(access_token=access_token, token_type="bearer", refresh_token=refresh_token)


@router.post("/register", response_model=User)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    user = await UserService.create(db, user_in)
    return user


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_data: TokenRefresh,
):
    try:
        payload = jwt.decode(
            refresh_data.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        token_type = payload.get("type")
        if token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        access_token = create_access_token(user_id)
        return Token(access_token=access_token, token_type="bearer")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
):
    revoke_token(str(current_user.id))
    return {"message": "Successfully logged out"}