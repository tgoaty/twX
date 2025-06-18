from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl, EmailStr, field_validator


class Settings(BaseSettings):
    DATABASE_URL: str
    URL: HttpUrl
    CLIENT_URL: HttpUrl
    JWT_ACCESS_SECRET: str
    JWT_REFRESH_SECRET: str
    MAIL_EMAIL: EmailStr
    MAIL_PASSWORD: str
    MAIL_SMTP_HOST: str
    MAIL_SMTP_PORT: int

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v.startswith("postgresql+asyncpg://"):
            raise ValueError("Must use asyncpg driver")
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
