from datetime import datetime

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.cruds.token import TokenCRUD
from app.cruds.user import UserCRUD
from app.schemas.auth import UserDtoScheme
from app.schemas.user import ChangePasswordScheme, ChangeBioScheme
from app.utils.security import verify_password, hash_password
from app.utils.token_utils import validate_refresh_token


class UserService:
    def __init__(self):
        self.token_crud = TokenCRUD()
        self.user_crud = UserCRUD()

    async def get_me(self, refresh_token: str, session: AsyncSession):
        user_data = validate_refresh_token(token=refresh_token)
        user = await self.user_crud.get_user_by_sid(user_data["sid"], session)
        user_dto = UserDtoScheme.model_validate(user)
        response = JSONResponse(content=jsonable_encoder(user_dto.model_dump()))
        return response

    async def change_password(
        self, refresh_token: str, data: ChangePasswordScheme, session: AsyncSession
    ):
        user_data = validate_refresh_token(token=refresh_token)
        user = await self.user_crud.get_user_by_sid(user_data["sid"], session)
        is_passwords_equals = verify_password(
            plain_password=data.old_password, hashed_password=user.hashed_password
        )
        if not is_passwords_equals:
            raise HTTPException(400, "Bad request")

        hashed = hash_password(data.new_password)

        if await self.user_crud.update_user_field(
            user.sid, field_name="hashed_password", value=hashed, session=session
        ):
            return JSONResponse(
                content={"message": "Password changed successfully"},
            )
        raise HTTPException(400, "Bad request")

    async def change_bio(
        self, refresh_token: str, data: ChangeBioScheme, session: AsyncSession
    ):
        user_data = validate_refresh_token(token=refresh_token)

        if await self.user_crud.update_user_field(
            user_data["sid"], field_name="bio", value=data.bio, session=session
        ):
            return JSONResponse(
                content={"message": "Bio changed successfully"},
            )
        raise HTTPException(400, "Bad request")

    async def update_last_active(self, refresh_token: str, session: AsyncSession):
        user_data = validate_refresh_token(token=refresh_token)
        await self.user_crud.update_user_field(
            user_data["sid"], "last_active", datetime.now(), session=session
        )
