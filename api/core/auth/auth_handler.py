import os
import jwt
import time
from typing import Dict

JWT_SECRET = os.getenv("AUTH_SECRET")
JWT_ALGORITHM = os.getenv("AUTH_ALGORITHM")
JWT_EXPIRE_TIME = 600


def signJWT(user_email: str, role: int) -> Dict[str, str]:
    """Encodes info from user to generate a JWT.
    It is returned within a dictionary.

    Args:
        user_email (str)
        role (int)

    Returns:
        Dict[str, str]
    """
    payload = {
        "user_email": user_email,
        "role": role,
        "expires": time.time() + JWT_EXPIRE_TIME
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {"access_token": token}


def decodeJWT(token: str) -> dict:
    """Decodes JWT.
    Returns None if token is expired.

    Args:
        token (str)

    Returns:
        dict: info extracted from token
        or None in case token expired
    """
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception:
        return {}


def get_payload(jwtoken: str) -> dict:
    """Returns decoded information from JWT
    or None in case something fails.

    Args:
        jwtoken (str)

    Returns:
        dict : info extracted from token
        or None in case something fails.
    """
    try:
        payload = decodeJWT(jwtoken)
    except Exception:
        payload = None
    return payload
