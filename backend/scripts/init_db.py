import asyncio
import sys

from sqlalchemy import text

from app.core.database import Base, engine

# Import models so SQLAlchemy registers all tables.
from app.models import academy, audit_log, machine, report, scan, session, target, user  # noqa: F401


async def wait_for_database(max_attempts: int = 30, delay_seconds: int = 2) -> None:
    for attempt in range(1, max_attempts + 1):
        try:
            async with engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            print("Database connection established.")
            return
        except Exception as exc:
            print(f"Waiting for database ({attempt}/{max_attempts}): {exc}")
            await asyncio.sleep(delay_seconds)

    print("Database is not ready.")
    sys.exit(1)


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables initialized.")


async def main() -> None:
    await wait_for_database()
    await create_tables()


if __name__ == "__main__":
    asyncio.run(main())
