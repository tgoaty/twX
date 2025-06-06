from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.services.auth.utils.get_user_dto_and_tokens import get_user_dto_and_tokens
from app.services.auth.utils.token_utils import validate_refresh_token, find_token


async def check_refresh_token(refresh_token: str, session: AsyncSession):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_data = validate_refresh_token(token=refresh_token)

    token_from_db = await find_token(refresh_token=refresh_token, session=session)

    if not user_data or not token_from_db:
        raise HTTPException(status_code=401, detail="Unauthorized")

    result = await session.execute(select(User).where(User.sid == user_data["sid"]))
    user = result.scalars().first()
    response = await get_user_dto_and_tokens(session, user)
    return response
