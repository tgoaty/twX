from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User

from sqlalchemy import select


async def activate(activation_link: str, session: AsyncSession):
    result = await session.execute(
        select(User).where(User.activation_link == activation_link)
    )
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail=f"The activation link {activation_link} does not exist",
        )

    user.is_activated = True

    await session.commit()
    await session.refresh(user)
