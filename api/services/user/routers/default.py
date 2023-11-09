from fastapi import APIRouter
from core.schemas.user import User

CLASS_TAG = "USERS_API"
users_router = APIRouter()


@users_router.get("/")
async def get_user_list() -> list[dict]:
    return [{"name": "Admin"}]
