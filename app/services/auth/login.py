from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.services.auth.utils.get_user_dto_and_tokens import get_user_dto_and_tokens
from app.services.auth.utils.security import verify_password


async def login(email, password, session: AsyncSession):
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    is_passwords_equals = verify_password(
        plain_password=password, hashed_password=user.hashed_password
    )

    if not is_passwords_equals:
        raise HTTPException(status_code=400, detail="Password does not match")

    response = await get_user_dto_and_tokens(session, user)
    return response
