import uuid
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class UserDto(BaseModel):
    username: str
    email: EmailStr
    sid: uuid.UUID
    is_activated: bool
    bio: str | None
    avatar_url: str | None
    created_at: datetime | None
    last_active: datetime | None

    model_config = {"from_attributes": True}


class RegistrationRequest(BaseModel):
    username: str = Field(..., min_length=5, max_length=50, description="Username")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(
        ..., min_length=8, max_length=128, description="Password from 8 characters"
    )


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
