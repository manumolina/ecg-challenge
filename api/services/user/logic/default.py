from core.auth.auth_handler import signJWT
from core.utils import create_random_password, hash_string
from services.user.schemas.user import (
    User, UserImport, UserLoginSchema, UserView
)
from services.user.data_sources.default import UserData


class UserLogic:
    @staticmethod
    def new(user: UserImport):
        new_user = user.__dict__
        # password hashed
        passw = create_random_password()
        new_user["password"] = hash_string(passw)
        UserData.insert(User(**new_user))
        # original password
        new_user["password"] = passw
        return new_user

    @staticmethod
    def get_all():
        return [UserView(**user.__dict__) for user in UserData.get({})]

    @staticmethod
    def check_user(user: UserLoginSchema):
        user_validated = UserData.validate_password_by_email(
            email=user.email,
            password=user.password
        )
        if not user_validated:
            return False
        return signJWT(user.email, user_validated["role"])

    @staticmethod
    def user_has_role(email: str, role: int):
        return UserData.validate_user_has_role_by_email(
            email, role
        )
