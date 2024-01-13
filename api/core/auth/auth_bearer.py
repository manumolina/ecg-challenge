from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.auth.auth_handler import decodeJWT
from libs.logger import logger
from services.user.logic.user import UserLogic


class JWTBearer(HTTPBearer):
    def __init__(self, only_admin: bool = None, auto_error: bool = True):
        self.only_admin = only_admin
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self,
        ).__call__(request)

        # not allowed without valid credentials
        if not credentials:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code.",
            )

        # not allowed without valid token
        if not credentials.scheme == "Bearer":
            raise HTTPException(
                status_code=403, detail="Invalid authentication scheme.",
            )
        if not self.verify_jwt(credentials.credentials):
            raise HTTPException(
                status_code=403, detail="Invalid token or expired token.",
            )

        # not allowed without valid role
        if self.only_admin is True and not self.verify_is_admin(
            credentials.credentials,
        ):
            raise HTTPException(
                status_code=403,
                detail="Invalid user role. Only administrators allowed.",
            )
        if self.only_admin is False and self.verify_is_admin(
            credentials.credentials,
        ):
            raise HTTPException(
                status_code=403,
                detail="Invalid user role. Not allowed to administrators.",
            )
        return credentials.credentials


    def verify_jwt(self, jwtoken: str) -> bool:
        """Checks if JWT is valid decoding it.

        Args:
        ----
            jwtoken (str)

        Returns:
        -------
            bool: result of the verification
        """
        try:
            payload = decodeJWT(jwtoken)
        except Exception as e:
            logger.exception(e)
            payload = None
        return bool(payload)

    def verify_is_admin(self, jwtoken: str) -> bool:
        """Checks if JWT is valid decoding it and checks if it contains the admin.

        Args:
        ----
            jwtoken (str)

        Returns:
        -------
            bool: result of the verification
        """
        result: bool = False
        adminRole: int = 99
        try:
            payload = decodeJWT(jwtoken)
            # Checking session role
            if payload["role"] != adminRole:
                return False

            # Double check with DB
            result = UserLogic.user_has_role(
                email=payload["user_email"], role=adminRole,
            )
        except Exception as e:
            logger.exception(e)
            return False
        return result
