from sqlalchemy.ext.asyncio import AsyncSession

from app.services.auth.utils.token_utils import remove_token


async def logout(session: AsyncSession, refresh_token: str):
    token = await remove_token(session=session, refresh_token=refresh_token)
    return token
