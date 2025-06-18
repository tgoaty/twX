from fastapi import APIRouter, Depends, Cookie, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.schemas.auth import (
    RegistrationScheme,
    LoginScheme,
    UserDtoScheme,
    SuccessResponse,
)
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/registration", response_model=SuccessResponse)
async def registration(
    data: RegistrationScheme,
    session: AsyncSession = Depends(get_session),
    service: AuthService = Depends(AuthService),
):
    return await service.registration(data, session)


@router.post("/login", response_model=UserDtoScheme)
async def login(
    data: LoginScheme,
    session: AsyncSession = Depends(get_session),
    service: AuthService = Depends(AuthService),
):
    return await service.login(data, session)


@router.post("/logout", response_model=SuccessResponse)
async def logout(
    refresh_token: str = Cookie(...),
    session: AsyncSession = Depends(get_session),
    service: AuthService = Depends(AuthService),
):
    return await service.logout(refresh_token, session)


@router.get("/activate", response_model=None)
async def activate_link(
    token: str = Query(...),
    session: AsyncSession = Depends(get_session),
    service: AuthService = Depends(AuthService),
):
    return await service.activate(token, session)


@router.get("/refresh", response_model=UserDtoScheme)
async def refresh(
    refresh_token: str = Cookie(...),
    session: AsyncSession = Depends(get_session),
    service: AuthService = Depends(AuthService),
):
    return await service.refresh(refresh_token, session)
