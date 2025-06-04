from fastapi import APIRouter

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register")
async def register():
    pass


@router.post("/login")
async def login():
    pass
