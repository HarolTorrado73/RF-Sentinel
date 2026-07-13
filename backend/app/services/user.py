from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


class UserService:
    @staticmethod
    async def get(db: AsyncSession, user_id: int) -> User | None:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_multi(db: AsyncSession) -> list[User]:
        result = await db.execute(select(User))
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, user_in: UserCreate) -> User:
        user = User(
            email=user_in.email,
            username=user_in.username,
            hashed_password=get_password_hash(user_in.password),
            full_name=user_in.full_name,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def update(db: AsyncSession, user_id: int, user_in: UserUpdate) -> User:
        user = await UserService.get(db, user_id)
        if not user:
            raise ValueError("User not found")
        
        if user_in.email:
            user.email = user_in.email
        if user_in.username:
            user.username = user_in.username
        if user_in.full_name:
            user.full_name = user_in.full_name
        if user_in.password:
            user.hashed_password = get_password_hash(user_in.password)
        if user_in.role:
            user.role = user_in.role
        
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def authenticate(
        db: AsyncSession, username: str, password: str
    ) -> User | None:
        user = await UserService.get_by_email(db, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    async def delete(db: AsyncSession, user_id: int) -> None:
        user = await UserService.get(db, user_id)
        if user:
            await db.delete(user)
            await db.commit()