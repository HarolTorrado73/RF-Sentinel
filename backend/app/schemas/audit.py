from pydantic import BaseModel


class AuditLogBase(BaseModel):
    action: str
    resource_type: str | None = None
    resource_id: str | None = None
    details: dict | None = None
    ip_address: str | None = None
    user_agent: str | None = None


class AuditLogCreate(AuditLogBase):
    pass


class AuditLogInDB(AuditLogBase):
    model_config = {"from_attributes": True}

    id: int
    user_id: int | None = None
    created_at: str | None = None


class AuditLog(AuditLogInDB):
    pass