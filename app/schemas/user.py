import uuid
from datetime import datetime

from pydantic import BaseModel


class UserDto(BaseModel):
    username: str
    email: str
    sid: uuid.UUID
    is_activated: bool
    bio: str | None
    avatar_url: str | None
    created_at: datetime | None
    last_active: datetime | None

    model_config = {"from_attributes": True}


class RegistrationRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str
