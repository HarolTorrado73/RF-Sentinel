from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.session import Session
from app.schemas.session import SessionCreate, SessionUpdate


class SessionService:
    @staticmethod
    async def get(db: AsyncSession, session_id: int) -> Session | None:
        result = await db.execute(select(Session).where(Session.id == session_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_multi(db: AsyncSession) -> list[Session]:
        result = await db.execute(select(Session))
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, session_in: SessionCreate) -> Session:
        session = Session(
            user_id=session_in.user_id,
            machine_id=session_in.machine_id,
            status=session_in.status,
        )
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session

    @staticmethod
    async def update(
        db: AsyncSession, session_id: int, session_in: SessionUpdate
    ) -> Session:
        session = await SessionService.get(db, session_id)
        if not session:
            raise ValueError("Session not found")

        if session_in.status:
            session.status = session_in.status
        if session_in.end_time:
            session.end_time = session_in.end_time

        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session

    @staticmethod
    async def delete(db: AsyncSession, session_id: int) -> None:
        session = await SessionService.get(db, session_id)
        if session:
            await db.delete(session)
            await db.commit()