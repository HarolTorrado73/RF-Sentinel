from pydantic import BaseModel, Field


class SessionBase(BaseModel):
    user_id: int | None = None
    machine_id: int | None = None
    status: str = Field(default="active", pattern="^(active|paused|closed)$")


class SessionCreate(SessionBase):
    user_id: int


class SessionUpdate(BaseModel):
    status: str | None = None
    end_time: str | None = None


class SessionInDB(SessionBase):
    model_config = {"from_attributes": True}

    id: int
    start_time: str | None = None
    end_time: str | None = None
    created_at: str | None = None


class Session(SessionInDB):
    pass