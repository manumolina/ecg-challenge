from fastapi import APIRouter, Body, Depends, Request
from core.auth.auth_bearer import JWTBearer
from services.user.exceptions import UserErrorSignIn
from services.user.logic.user import UserLogic
from services.user.schemas.user import UserImport, UserLoginSchema

CLASS_TAG = "USERS_API"
PATH_PREFIX = "/admin"
users_router = APIRouter()


@users_router.post("/login")
async def user_login(user: UserLoginSchema = Body(...)):
    result = UserLogic().check_user(user)
    if not result:
        raise UserErrorSignIn()
    return result


@users_router.get("/", dependencies=[Depends(JWTBearer(only_admin=True))])
async def get_user_list() -> list[dict]:
    return UserLogic.get_all()


# only admin can add other admins
@users_router.post("/", dependencies=[Depends(JWTBearer(only_admin=True))])
async def set_user(
    request: Request,
    user: UserImport
) -> dict:
    result = UserLogic.new(user)
    return {
        "message": "User created. Save your password in a safe place.",
        "data": result
    }
