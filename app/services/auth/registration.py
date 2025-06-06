import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.services.auth.utils.get_user_dto_and_tokens import get_user_dto_and_tokens
from app.services.auth.utils.security import hash_password
from app.services.auth.utils.send_activation_mail import send_activation_mail
from app.config import URL


async def registration(username: str, email: str, password: str, session: AsyncSession):
    result = await session.execute(select(User).where(User.email == email))
    existing_user = result.scalars().first()
    if existing_user:
        raise Exception(f"User with email {email} already exists")

    hashed = hash_password(password)
    activation_link = str(uuid.uuid4())

    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed,
        activation_link=activation_link,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    await send_activation_mail(email, f"{URL}/api/user/activate/{activation_link}")

    response = await get_user_dto_and_tokens(session, new_user)
    return response
