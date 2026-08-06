"""Inicializa PostgreSQL: espera, migraciones Alembic y semillas."""

from __future__ import annotations

import asyncio
import subprocess
import sys
from pathlib import Path

from sqlalchemy import inspect, text

from app.core.database import engine

# Import models so metadata is available for inspection helpers.
from app.models import academy, audit_log, machine, report, scan, session, target, user  # noqa: F401

BACKEND_ROOT = Path(__file__).resolve().parents[1]


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


def run_alembic(*args: str) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "alembic", *args],
        cwd=BACKEND_ROOT,
        check=False,
    )
    if result.returncode != 0:
        print(f"Alembic command failed: alembic {' '.join(args)}")
        sys.exit(result.returncode)


async def _has_alembic_version() -> bool:
    async with engine.connect() as conn:

        def _check(sync_conn):
            inspector = inspect(sync_conn)
            return inspector.has_table("alembic_version")

        return await conn.run_sync(_check)


async def _has_application_tables() -> bool:
    async with engine.connect() as conn:

        def _check(sync_conn):
            inspector = inspect(sync_conn)
            return inspector.has_table("users")

        return await conn.run_sync(_check)


async def migrate() -> None:
    has_version = await _has_alembic_version()
    has_tables = await _has_application_tables()

    if has_tables and not has_version:
        # Esquema creado previamente con create_all: marcar como migrado.
        run_alembic("stamp", "head")
        print("Existing schema stamped to Alembic head.")
        return

    run_alembic("upgrade", "head")
    print("Alembic migrations applied (upgrade head).")


async def run_seeds() -> None:
    # Al ejecutar `python scripts/init_db.py`, sys.path incluye `scripts/`.
    from seed_db import main as seed_main

    await seed_main()


async def main() -> None:
    await wait_for_database()
    await migrate()
    await run_seeds()


if __name__ == "__main__":
    asyncio.run(main())
