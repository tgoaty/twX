from fastapi import APIRouter
from app.services import user

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/user/{username}")
async def get_user(username: str):
    await user.get_user_info(username)


@router.post("/bio")
async def change_bio(bio: str):
    await user.change_user_bio(bio)


@router.post("/avatar")
async def change_avatar(avatar: str):
    await user.change_avatar(avatar)


@router.get("/update-time")
async def update_last_time():
    await user.update_last_active_time()
