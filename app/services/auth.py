from urllib.parse import quote_plus
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse, RedirectResponse
from app.cruds.token import TokenCRUD
from app.models import User
from app.schemas.auth import RegistrationScheme, LoginScheme, UserDtoScheme
from app.utils.security import hash_password, verify_password
from app.utils.mail import send_activation_mail
from app.core.config import settings
from app.cruds.user import UserCRUD
from app.utils.token_utils import validate_refresh_token, generate_tokens


class AuthService:
    def __init__(self):
        self.user_crud = UserCRUD()
        self.token_crud = TokenCRUD()

    async def registration(self, data: RegistrationScheme, session: AsyncSession):
        existing_user = await self.user_crud.get_user_by_email(data.email, session)
        if existing_user:
            raise HTTPException(400, f"User with email {data.email} already exists")

        hashed = hash_password(data.password)

        new_user = User(
            username=data.username,
            email=str(data.email),
            hashed_password=hashed,
        )

        await self.user_crud.create_user(new_user, session)
        await send_activation_mail(
            data.email, f"{settings.URL}/api/auth/activate?token={quote_plus(hashed)}"
        )

        return JSONResponse(
            content={"message": "Registration successful, Email send"},
        )

    async def login(self, data: LoginScheme, session: AsyncSession):
        user = await self.user_crud.get_user_by_email(data.email, session)
        if not user:
            raise HTTPException(status_code=400, detail="User not found")

        is_passwords_equals = verify_password(
            plain_password=data.password, hashed_password=user.hashed_password
        )

        if not is_passwords_equals:
            raise HTTPException(400, "Bad request")

        return await self.get_user_dto_and_tokens(user, session)

    async def logout(self, refresh_token: str, session: AsyncSession):
        await self.token_crud.remove_token(refresh_token, session)
        response = JSONResponse(content={"detail": "Logged out"})
        response.delete_cookie("refresh_token")
        return response

    async def activate(self, activation_link: str, session: AsyncSession):
        await self.user_crud.activate_user(activation_link, session)
        return RedirectResponse(settings.CLIENT_URL)

    async def refresh(self, refresh_token: str, session: AsyncSession):
        user_data = validate_refresh_token(token=refresh_token)
        token_from_db = await self.token_crud.find_token(refresh_token, session)
        if not user_data or not token_from_db:
            raise HTTPException(status_code=401, detail="Unauthorized")

        user = await self.user_crud.get_user_by_sid(user_data["sid"], session)
        response = await self.get_user_dto_and_tokens(user, session)
        return response

    async def get_user_dto_and_tokens(self, user: User, session: AsyncSession):
        user_dto = UserDtoScheme.model_validate(user)
        tokens = await generate_tokens(user_dto)
        await self.token_crud.update_token(user.sid, tokens, session)

        response = JSONResponse(content=jsonable_encoder(user_dto.model_dump()))
        response.set_cookie(
            key="refresh_token",
            value=tokens.refresh_token,
            httponly=True,
            max_age=60 * 60 * 24 * 30,
        )
        response.set_cookie(
            key="access_token",
            value=tokens.access_token,
            httponly=True,
            max_age=60 * 30,
        )
        return response
