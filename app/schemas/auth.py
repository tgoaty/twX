from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

from app.schemas.base import CustomBaseModal


class TokenPayloadScheme(BaseModel):
    sid: UUID
    username: str
    email: EmailStr
    exp: int | None = None
    iat: int | None = None
    nbf: int | None = None


class UserDtoScheme(CustomBaseModal):
    sid: UUID
    username: str
    email: EmailStr
    is_activated: bool
    bio: str | None
    last_active: datetime


class RegistrationScheme(BaseModel):
    username: str = Field(..., min_length=5, max_length=50, description="Username")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(
        ..., min_length=8, max_length=128, description="Password from 8 characters"
    )


class LoginScheme(BaseModel):
    email: EmailStr
    password: str


class TokensScheme(BaseModel):
    access_token: str
    refresh_token: str
