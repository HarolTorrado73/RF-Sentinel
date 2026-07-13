from pydantic import BaseModel, Field, ConfigDict


class TargetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    target_type: str = Field(..., pattern="^(ip|domain|cidr)$")
    value: str = Field(..., min_length=1, max_length=255)
    description: str | None = None


class TargetCreate(TargetBase):
    pass


class TargetUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class TargetInDB(TargetBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    owner_id: int | None = None


class Target(TargetInDB):
    pass