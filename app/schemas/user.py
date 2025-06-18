from pydantic import BaseModel, Field


class ChangePasswordScheme(BaseModel):
    old_password: str
    new_password: str = Field(
        ..., min_length=8, max_length=128, description="Password from 8 characters"
    )


class ChangeBioScheme(BaseModel):
    bio: str = Field(..., min_length=1, max_length=256, description="Bio description")
