from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse, RedirectResponse
from app.db import get_session
from app.schemas.auth import RegistrationRequest, LoginRequest
from app.services import auth
from app.config import CLIENT_URL

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/registration")
async def registration(
    data: RegistrationRequest, session: AsyncSession = Depends(get_session)
):
    user_data = await auth.registration(
        username=data.username,
        email=data.email,
        password=data.password,
        session=session,
    )
    response = JSONResponse(
        content={
            "access_token": user_data["access_token"],
            "user": user_data["user"],
        }
    )
    response.set_cookie(
        key="refresh_token",
        value=user_data["refresh_token"],
        httponly=True,
        max_age=60 * 60 * 24 * 30,
    )
    return response


@router.post("/login")
async def login(
    data: LoginRequest,
    session: AsyncSession = Depends(get_session),
):
    user_data = await auth.login(
        email=data.email, password=data.password, session=session
    )

    response = JSONResponse(
        content={
            "access_token": user_data["access_token"],
            "user": user_data["user"],
        }
    )
    response.set_cookie(
        key="refresh_token",
        value=user_data["refresh_token"],
        httponly=True,
        max_age=60 * 60 * 24 * 30,
    )
    return response


@router.post("/logout")
async def logout(request: Request, session: AsyncSession = Depends(get_session)):
    refresh_token = request.cookies.get("refresh_token")
    token = await auth.logout(session, refresh_token)
    response = JSONResponse(content={"token": token})
    response.delete_cookie("refresh_token")
    return response


@router.get("/activate/{link}")
async def activate_link(link: str, session: AsyncSession = Depends(get_session)):
    await auth.activate(activation_link=link, session=session)
    return RedirectResponse(CLIENT_URL)


@router.get("/refresh")
async def refresh(request: Request, session: AsyncSession = Depends(get_session)):
    refresh_token = request.cookies.get("refresh_token")
    new_refresh_token = await auth.check_refresh_token(refresh_token, session=session)

    response = JSONResponse(
        content={
            "access_token": new_refresh_token["access_token"],
            "user": new_refresh_token["user"],
        }
    )
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token["refresh_token"],
        httponly=True,
        max_age=60 * 60 * 24 * 30,
    )
    return response
