from pydantic import BaseModel, Field
from datetime import datetime


class ScanBase(BaseModel):
    target_id: int
    scan_type: str = Field(..., pattern="^(ping|tcp|udp|service|os)$")


class ScanCreate(ScanBase):
    pass


class ScanUpdate(BaseModel):
    status: str | None = None


class ScanInDB(ScanBase):
    model_config = {"from_attributes": True}

    id: int
    status: str
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_by_id: int | None = None
    results: dict | None = None
    error_message: str | None = None


class Scan(ScanInDB):
    pass