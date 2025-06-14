from sqlalchemy import select

from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User


class UserCRUD:
    def __init__(self):
        pass

    async def create_user(self, user: User, session: AsyncSession):
        session.add(user)
        await session.commit()
        await session.refresh(user)

    async def get_user_by_email(self, user_email: EmailStr, session: AsyncSession):
        result = await session.execute(select(User).where(User.email == user_email))
        return result.scalars().first()

    async def get_user_by_sid(self, user_sid: int, session: AsyncSession):
        result = await session.execute(select(User).where(User.sid == user_sid))
        return result.scalars().first()

    async def activate_user(self, activation_link: str, session: AsyncSession):
        result = await session.execute(
            select(User).where(User.hashed_password == activation_link)
        )
        user = result.scalars().first()

        if user:
            user.is_activated = True
            await session.commit()
            await session.refresh(user)
