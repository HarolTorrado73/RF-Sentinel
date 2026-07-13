from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from app.models.target import Target
from app.schemas.target import TargetCreate, TargetUpdate


class TargetService:
    @staticmethod
    async def get(db: AsyncSession, target_id: int) -> Target | None:
        result = await db.execute(select(Target).where(Target.id == target_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_multi(db: AsyncSession) -> list[Target]:
        result = await db.execute(select(Target))
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, target_in: TargetCreate, owner_id: int) -> Target:
        target = Target(
            name=target_in.name,
            target_type=target_in.target_type,
            value=target_in.value,
            description=target_in.description,
            owner_id=owner_id,
        )
        db.add(target)
        await db.commit()
        await db.refresh(target)
        return target

    @staticmethod
    async def update(db: AsyncSession, target_id: int, target_in: TargetUpdate) -> Target:
        target = await TargetService.get(db, target_id)
        if not target:
            raise ValueError("Target not found")
        
        if target_in.name:
            target.name = target_in.name
        if target_in.description:
            target.description = target_in.description
        
        db.add(target)
        await db.commit()
        await db.refresh(target)
        return target

    @staticmethod
    async def delete(db: AsyncSession, target_id: int) -> None:
        target = await TargetService.get(db, target_id)
        if target:
            await db.delete(target)
            await db.commit()