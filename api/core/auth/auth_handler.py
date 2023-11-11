import os
import jwt
import time
from typing import Dict

JWT_SECRET = os.getenv("AUTH_SECRET")
JWT_ALGORITHM = os.getenv("AUTH_ALGORITHM")
JWT_EXPIRE_TIME = 600


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: str, role: int) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "role": role,
        "expires": time.time() + JWT_EXPIRE_TIME
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception:
        return {}
