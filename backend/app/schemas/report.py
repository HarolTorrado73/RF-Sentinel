from pydantic import BaseModel, Field
from datetime import datetime


class ReportBase(BaseModel):
    scan_id: int | None = None
    title: str = Field(..., min_length=1, max_length=255)
    report_type: str = Field(..., pattern="^(pdf|csv|json)$")


class ReportCreate(ReportBase):
    pass


class ReportInDB(ReportBase):
    model_config = {"from_attributes": True}

    id: int
    file_path: str | None = None
    created_by_id: int | None = None
    created_at: datetime


class Report(ReportInDB):
    pass