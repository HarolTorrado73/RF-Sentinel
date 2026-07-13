from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str | None = None


class TokenPayload(BaseModel):
    sub: int | None = None
    exp: int | None = None
    type: str | None = None


class TokenRefresh(BaseModel):
    refresh_token: str