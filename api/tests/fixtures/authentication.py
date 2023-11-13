

from dataclasses import dataclass

import pytest
from fastapi import Request
from fastapi.testclient import TestClient

from application_factory import create_api
from core.auth.auth_bearer import JWTBearer
from core.auth.auth_handler import signJWT
from tests.utils.constants import JWT_TOKEN, TEST_USER


@dataclass
class JWTTokenParameter:
    jwt_token: str
    user_name: str


def test_validate_jwt_token(request: Request):
    return JWTTokenParameter(jwt_token=JWT_TOKEN, user_name=TEST_USER)


def test_invalid_jwt_token(request: Request):
    return JWTTokenParameter(jwt_token="invalid Jwt", user_name="test invalid user")


def test_valid_user(request: Request):
    return TEST_USER


def test_invalid_user(request: Request):
    return "test invalid user"


@pytest.fixture()
def authenticate_mock_client():
    app = create_api()
    app.dependency_overrides[JWTBearer] = test_valid_user

    return TestClient(app)


@pytest.fixture()
def authenticate_mock_invalid_client():
    app = create_api()
    app.dependency_overrides[JWTBearer] = test_invalid_user

    return TestClient(app)


def access_token(user):
    access_token = signJWT(user)
    return access_token["access_token"]


@pytest.fixture()
def get_request_header():
    test_user = {
        "_id": "630cddc46b642d5913e5d09d",
        "email": "user.1.test@test.com",
        "expires": time.time() + 3600,
    }
    token = access_token(test_user)
    return {"Authorization": f"Bearer {token}"}
