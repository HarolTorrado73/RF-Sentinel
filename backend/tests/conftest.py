import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Test env vars must be set before importing app settings.
os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("SECRET_KEY", "test-secret-key")

from app.api import deps
from app.core.database import Base
from app.main import app
from app.schemas.user import UserCreate
from app.services.user import UserService

# Ensure SQLAlchemy metadata includes all model tables.
from app.models import academy, audit_log, machine, report, scan, session, target, user  # noqa: F401


@pytest.fixture()
async def db_sessionmaker(tmp_path: Path) -> async_sessionmaker[AsyncSession]:
    db_file = tmp_path / "test.db"
    database_url = f"sqlite+aiosqlite:///{db_file}"

    engine = create_async_engine(database_url, future=True)
    sessionmaker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield sessionmaker

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture()
def client(db_sessionmaker: async_sessionmaker[AsyncSession]) -> TestClient:
    async def override_get_db():
        async with db_sessionmaker() as session:
            yield session

    app.dependency_overrides[deps.get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture()
async def admin_user(db_sessionmaker: async_sessionmaker[AsyncSession]) -> dict[str, str | int]:
    async with db_sessionmaker() as session:
        user = await UserService.create(
            session,
            UserCreate(
                email="admin@example.com",
                username="admin",
                full_name="Admin User",
                password="adminpass123",
            ),
        )
        user.role = "admin"
        session.add(user)
        await session.commit()
        await session.refresh(user)

        return {
            "id": user.id,
            "email": user.email,
            "password": "adminpass123",
        }


@pytest.fixture()
def auth_headers(client: TestClient, admin_user: dict[str, str | int]) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": str(admin_user["email"]),
            "password": str(admin_user["password"]),
        },
    )
    assert response.status_code == 200

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
