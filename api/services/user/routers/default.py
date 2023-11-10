from fastapi import APIRouter, Request
from services.user.logic.default import UserLogic
from services.user.schemas.user import UserImport

CLASS_TAG = "USERS_API"
users_router = APIRouter()


@users_router.get("/")
async def get_user_list() -> list[dict]:
    return [{"name": "Admin"}]


@users_router.post("/")
async def set_user(
    request: Request,
    user: UserImport
) -> dict:
    result = UserLogic().new(user)
    return user
