"""Repositorio de capturas."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from rf_sentinel.database.models.capture import Capture


class CaptureRepository:
    """Repositorio CRUD para capturas."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, capture: Capture) -> Capture:
        self.db.add(capture)
        await self.db.commit()
        await self.db.refresh(capture)
        return capture

    async def get(self, capture_id: int) -> Capture | None:
        result = await self.db.execute(select(Capture).where(Capture.id == capture_id))
        return result.scalar_one_or_none()

    async def list(self, limit: int = 100, offset: int = 0) -> list[Capture]:
        result = await self.db.execute(select(Capture).limit(limit).offset(offset))
        return list(result.scalars().all())

    async def delete(self, capture_id: int) -> bool:
        capture = await self.get(capture_id)
        if not capture:
            return False
        await self.db.delete(capture)
        await self.db.commit()
        return True
