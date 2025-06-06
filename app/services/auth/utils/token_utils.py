from fastapi import HTTPException
from jose import jwt
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, UUID

from app.config import JWT_ACCESS_SECRET, JWT_REFRESH_SECRET
from app.models import Token


async def generate_tokens(payload: dict) -> dict:
    now = datetime.now(timezone.utc)

    access_payload = payload.copy()
    access_payload["exp"] = now + timedelta(minutes=30)
    access_token = jwt.encode(access_payload, JWT_ACCESS_SECRET, algorithm="HS256")

    refresh_payload = payload.copy()
    refresh_payload["exp"] = now + timedelta(days=30)
    refresh_token = jwt.encode(refresh_payload, JWT_REFRESH_SECRET, algorithm="HS256")

    return {"access_token": access_token, "refresh_token": refresh_token}


async def save_token(session: AsyncSession, user: UUID, refresh_token: str):
    result = await session.execute(select(Token).where(Token.user == user))
    token_data = result.scalars().first()

    if token_data:
        token_data.refresh_token = refresh_token
    else:
        token_data = Token(user=user, refresh_token=refresh_token)
        session.add(token_data)
    await session.commit()
    return token_data


async def remove_token(session: AsyncSession, refresh_token: str):
    result = await session.execute(
        select(Token).where(Token.refresh_token == refresh_token)
    )
    token_data = result.scalars().first()

    if not token_data:
        raise HTTPException(status_code=404, detail="Token not found")

    await session.delete(token_data)
    await session.commit()
    return token_data.refresh_token


def validate_access_token(token: str):
    try:
        user_data = jwt.decode(token, JWT_ACCESS_SECRET, algorithms=["HS256"])
        return user_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Token not found: {e}")


def validate_refresh_token(token: str):
    try:
        user_data = jwt.decode(token, JWT_REFRESH_SECRET, algorithms=["HS256"])
        return user_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Token not found: {e}")


async def find_token(session: AsyncSession, refresh_token: str):
    result = await session.execute(
        select(Token).where(Token.refresh_token == refresh_token)
    )
    token_data = result.scalars().first()

    if not token_data:
        raise HTTPException(status_code=404, detail="Token not found")

    return token_data.refresh_token
