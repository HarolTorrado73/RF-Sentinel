"""Modelos de base de datos para RF Sentinel."""

from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///rf_sentinel.db"
SYNC_DATABASE_URL = "sqlite:///rf_sentinel.db"


class Base(DeclarativeBase):
    """Base para modelos SQLAlchemy."""

    pass


class Capture(Base):
    """Modelo para capturas de espectro."""

    __tablename__ = "captures"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    timestamp: datetime = Column(DateTime, default=datetime.utcnow, index=True)
    center_frequency: float = Column(Float, nullable=False)
    sample_rate: float = Column(Float, nullable=False)
    bandwidth: float | None = Column(Float, nullable=True)
    duration: float = Column(Float, nullable=False)
    filename: str | None = Column(String(255), nullable=True)
    peak_power: float | None = Column(Float, nullable=True)
    noise_floor: float | None = Column(Float, nullable=True)
    data: bytes | None = Column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<Capture {self.id}: {self.center_frequency}MHz>"


class Signal(Base):
    """Modelo para señales detectadas."""

    __tablename__ = "signals"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    capture_id: int = Column(Integer, nullable=False, index=True)
    frequency: float = Column(Float, nullable=False)
    bandwidth: float = Column(Float, nullable=False)
    power: float = Column(Float, nullable=False)
    modulation: str | None = Column(String(50), nullable=True)
    classification: str | None = Column(String(100), nullable=True)
    confidence: float | None = Column(Float, nullable=True)
    timestamp: datetime = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Signal {self.id}: {self.frequency}MHz>"


# Engines
async_engine = create_async_engine(DATABASE_URL, echo=False)
sync_engine = create_engine(SYNC_DATABASE_URL, echo=False)

# Sessions
AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
SyncSessionLocal = sessionmaker(sync_engine, class_=Session, expire_on_commit=False)


async def get_db() -> AsyncSession:
    """Obtiene sesión de base de datos async."""
    async with AsyncSessionLocal() as session:
        yield session


def init_db() -> None:
    """Inicializa la base de datos."""
    Base.metadata.create_all(sync_engine)
