"""Repositorio de señales."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from rf_sentinel.database.models.signal import Signal


class SignalRepository:
    """Repositorio CRUD para señales."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, signal: Signal) -> Signal:
        self.db.add(signal)
        await self.db.commit()
        await self.db.refresh(signal)
        return signal

    async def get(self, signal_id: int) -> Signal | None:
        result = await self.db.execute(select(Signal).where(Signal.id == signal_id))
        return result.scalar_one_or_none()

    async def get_by_capture(self, capture_id: int) -> list[Signal]:
        result = await self.db.execute(
            select(Signal).where(Signal.capture_id == capture_id)
        )
        return list(result.scalars().all())

    async def delete(self, signal_id: int) -> bool:
        signal = await self.get(signal_id)
        if not signal:
            return False
        await self.db.delete(signal)
        await self.db.commit()
        return True
