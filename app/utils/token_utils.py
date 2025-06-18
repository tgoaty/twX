from fastapi.encoders import jsonable_encoder
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from app.schemas.auth import UserDtoScheme, TokensScheme, TokenPayloadScheme


def create_access_token(payload: TokenPayloadScheme) -> str:
    now = datetime.now(timezone.utc)
    data = jsonable_encoder(
        payload.model_copy(
            update={
                "exp": int((now + timedelta(minutes=30)).timestamp()),
                "iat": int(now.timestamp()),
                "nbf": int(now.timestamp()),
            }
        ).model_dump()
    )

    return jwt.encode(data, settings.JWT_ACCESS_SECRET, algorithm="HS256")


def create_refresh_token(payload: TokenPayloadScheme) -> str:
    now = datetime.now(timezone.utc)
    data = jsonable_encoder(
        payload.model_copy(
            update={
                "exp": int((now + timedelta(days=30)).timestamp()),
                "iat": int(now.timestamp()),
                "nbf": int(now.timestamp()),
            }
        ).model_dump()
    )

    return jwt.encode(data, settings.JWT_REFRESH_SECRET, algorithm="HS256")


async def generate_tokens(user_dto: UserDtoScheme) -> TokensScheme:
    payload = TokenPayloadScheme(
        sid=user_dto.sid, username=user_dto.username, email=user_dto.email
    )
    return TokensScheme(
        access_token=create_access_token(payload),
        refresh_token=create_refresh_token(payload),
    )


def validate_access_token(token: str):
    user_data = jwt.decode(token, settings.JWT_ACCESS_SECRET, algorithms=["HS256"])
    return user_data


def validate_refresh_token(token: str):
    user_data = jwt.decode(token, settings.JWT_REFRESH_SECRET, algorithms=["HS256"])
    return user_data
