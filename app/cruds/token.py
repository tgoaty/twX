from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Token
from app.schemas.auth import TokensScheme


class TokenCRUD:
    def __init__(self):
        pass

    async def find_token(self, refresh_token: str, session: AsyncSession):
        result = await session.execute(
            select(Token).where(Token.refresh_token == refresh_token)
        )
        return result.scalars().first()

    async def get_token_by_user_sid(self, user_sid: str, session: AsyncSession):
        result = await session.execute(select(Token).where(Token.user_sid == user_sid))
        return result.scalars().first()

    async def update_token(
            self,
            user_sid: UUID,
            tokens: TokensScheme,
            session: AsyncSession,
    ):
        result = await session.execute(select(Token).where(Token.user_sid == user_sid))
        token_data = result.scalars().first()

        if token_data:
            token_data.refresh_token = tokens.refresh_token
            token_data.access_token = tokens.access_token
        else:
            token_data = Token(
                user_sid=user_sid,
                refresh_token=tokens.refresh_token,
                access_token=tokens.access_token,
            )
            session.add(token_data)
        await session.commit()

    async def remove_token(self, refresh_token: str, session: AsyncSession):
        result = await session.execute(
            select(Token).where(Token.refresh_token == refresh_token)
        )
        token_data = result.scalars().first()

        await session.delete(token_data)
        await session.commit()
        return token_data.refresh_token
