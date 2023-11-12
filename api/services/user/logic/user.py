import uuid
from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param

from core.auth.auth_handler import signJWT, get_payload
from core.utils import create_random_password, hash_string
from services.user.schemas.user import (
    User, UserImport, UserLoginSchema, UserView
)
from api.services.user.data_sources.user import UserData


class UserLogic:
    @staticmethod
    def new(user: UserImport) -> dict:
        """Generates a new user.
        Steps:
        * creates random password
        * encrypts password
        * insert user in DB
        * returns user with non-encrypted password

        Args:
            user (UserImport): data to save in the DB

        Returns:
            dict: data to save including the new password
        """
        new_user = user.__dict__
        # password hashed
        passw = create_random_password()
        new_user["password"] = hash_string(passw)
        UserData.insert(User(**new_user))
        # original password
        new_user["password"] = passw
        return new_user

    @staticmethod
    def get_all() -> list[UserView]:
        """Method only allowed to admin users.
        Returns list of existing users in DB
        but with only non critical information.

        Returns:
            list[UserView]: list of users in DB
        """
        return [UserView(**user.__dict__) for user in UserData.get({})]

    @staticmethod
    def get_user_id_from_email(email: str) -> uuid.uuid4:
        """Returns User ID searching by email.

        Args:
            email (str): user email

        Returns:
            uuid.uuid4: User ID if exists
            or None if not.
        """
        user = UserData.get(
            where={getattr(User, "email"): email},
            limit=1,
        )
        if not user:
            return None
        return user[0].__dict__["id"]

    @staticmethod
    def check_user(user: UserLoginSchema) -> str:
        """Checks if user (email + pass) are valids.
        If so, returns JWT using these data.

        Args:
            user (UserLoginSchema): Contains email and pass

        Returns:
            str: JWT in case credentials are valid
            or None if not.
        """
        user_validated = UserData.validate_password_by_email(
            email=user.email,
            password=user.password
        )
        if not user_validated:
            return None
        return signJWT(user.email, user_validated["role"])

    @staticmethod
    def user_has_role(email: str, role: int):
        """Checks if user contains the requested role.

        Args:
            email (str)
            role (int)

        Returns:
            list: list with a single user from DB
            if contains the requested role
            or empty list if not.
        """
        return UserData.validate_user_has_role_by_email(
            email, role
        )

    def get_user_id_from_request(
        self, request: Request
    ) -> uuid.uuid4:
        """Extract current token if exists from request header.
        Search for the associated user id and returns it.

        Args:
            request (Request)

        Returns:
            uuid.uuid4: user id associated to the email in JWT.
        """
        header_authorization: str = request.headers.get("Authorization")
        _, header_param = get_authorization_scheme_param(
                header_authorization
        )
        payload = get_payload(header_param)
        return self.get_user_id_from_email(payload["user_email"])
