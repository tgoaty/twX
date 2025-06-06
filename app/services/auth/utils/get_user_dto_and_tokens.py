from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserDto
from app.services.auth.utils.token_utils import generate_tokens, save_token


async def get_user_dto_and_tokens(session: AsyncSession, user):
    user_dto = UserDto.model_validate(user)

    tokens = await generate_tokens(jsonable_encoder(user_dto.model_dump()))
    await save_token(session, user_dto.sid, tokens["refresh_token"])
    return {
        "refresh_token": tokens["refresh_token"],
        "access_token": tokens["access_token"],
        "user": jsonable_encoder(user_dto.model_dump()),
    }
