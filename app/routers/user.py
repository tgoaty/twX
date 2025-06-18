from fastapi import APIRouter, Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.auth import UserDtoScheme, SuccessResponse
from app.schemas.user import ChangePasswordScheme, ChangeBioScheme
from app.services.user import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me", response_model=UserDtoScheme)
async def get_me(
    refresh_token: str = Cookie(...),
    session: AsyncSession = Depends(get_session),
    service: UserService = Depends(UserService),
):
    return await service.get_me(refresh_token=refresh_token, session=session)


@router.patch("/change_password", response_model=SuccessResponse)
async def change_password(
    data: ChangePasswordScheme,
    refresh_token: str = Cookie(...),
    session: AsyncSession = Depends(get_session),
    service: UserService = Depends(UserService),
):
    return await service.change_password(
        refresh_token=refresh_token, data=data, session=session
    )


@router.patch("/change_bio", response_model=SuccessResponse)
async def change_bio(
    data: ChangeBioScheme,
    refresh_token: str = Cookie(...),
    session: AsyncSession = Depends(get_session),
    service: UserService = Depends(UserService),
):
    return await service.change_bio(
        refresh_token=refresh_token, data=data, session=session
    )


@router.patch("/last_active", response_model=None)
async def last_active(
    refresh_token: str = Cookie(...),
    session: AsyncSession = Depends(get_session),
    service: UserService = Depends(UserService),
):
    await service.update_last_active(refresh_token=refresh_token, session=session)
