"""Semillas iniciales de producción/desarrollo."""

from __future__ import annotations

import asyncio
import os

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.core.security import get_password_hash
from app.models.machine import Machine
from app.models.user import User
from app.services.academy import AcademyService


async def seed_academy() -> None:
    async with AsyncSessionLocal() as db:
        await AcademyService.seed_content(db)
    print("Academy seed applied.")


async def seed_admin_user() -> None:
    email = os.getenv("SEED_ADMIN_EMAIL", "admin@rf-sentinel.local")
    username = os.getenv("SEED_ADMIN_USERNAME", "admin")
    password = os.getenv("SEED_ADMIN_PASSWORD", "adminchangeme")
    full_name = os.getenv("SEED_ADMIN_FULL_NAME", "RF Sentinel Admin")

    async with AsyncSessionLocal() as db:
        existing = await db.execute(select(User).where(User.email == email))
        if existing.scalar_one_or_none():
            print(f"Admin user already exists: {email}")
            return

        user = User(
            email=email,
            username=username,
            hashed_password=get_password_hash(password),
            full_name=full_name,
            is_active=True,
            is_superuser=True,
            role="admin",
        )
        db.add(user)
        await db.commit()
        print(f"Admin user created: {email}")


async def seed_lab_machine() -> None:
    async with AsyncSessionLocal() as db:
        existing = await db.execute(
            select(Machine).where(Machine.hostname == "lab-sdr-01")
        )
        if existing.scalar_one_or_none():
            print("Lab machine already exists: lab-sdr-01")
            return

        machine = Machine(
            hostname="lab-sdr-01",
            ip_address="10.0.0.10",
            operating_system="Linux",
            status="available",
        )
        db.add(machine)
        await db.commit()
        print("Lab machine seed applied: lab-sdr-01")


async def main() -> None:
    await seed_academy()
    await seed_admin_user()
    await seed_lab_machine()
    print("Initial seeds completed.")


if __name__ == "__main__":
    asyncio.run(main())
