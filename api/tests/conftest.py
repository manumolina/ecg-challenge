import pytest
from fastapi import Request
from fastapi.testclient import TestClient
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from unittest.mock import Mock

from application_factory import create_api
from core.auth.auth_bearer import JWTBearer
from core.auth.auth_handler import signJWT
from core.database import Database
from core.utils import create_random_password

from services.user.schemas.user import User, UserDBView
from services.ecg.schemas.ecg import ECGImport, ECGOutput
from tests.utils.constants import JWT_TOKEN, TEST_USER


def get_single_user_dict():
    random_string = create_random_password(10)
    return {
        "id": uuid4(),
        "created": datetime.now(),
        "updated": datetime.now(),
        "username": random_string,
        "email": f"{random_string}@idoven-challenge.com",
        "password": random_string,
        "disabled": False,
        "role": 0
    }


@pytest.fixture
def get_list_of_users():
    user_len = 3
    test_users = []
    for _ in range(user_len):
        test_users.append(UserDBView(**get_single_user_dict()))
    return test_users


@pytest.fixture
def get_list_of_new_users():
    user_len = 3
    test_users = []
    for _ in range(user_len):
        test_users.append(User(**get_single_user_dict()))
    return test_users


@pytest.fixture
def get_single_user():
    user = get_single_user_dict()
    return UserDBView(**user)


@pytest.fixture
def get_list_of_valid_ecgs():
    ecgs_len = 3
    test_ecgs = []
    for _ in range(ecgs_len):
        test_ecgs.append(ECGImport(**get_single_ecg()))
    return test_ecgs


@pytest.fixture
def get_list_of_valid_ecgs_output():
    ecgs_len = 3
    test_ecgs = []
    for _ in range(ecgs_len):
        test_ecgs.append(ECGOutput(**get_single_ecg()))
    return test_ecgs


@pytest.fixture
def get_list_of_invalid_ecgs():
    ecgs_len = 3
    test_ecgs = []
    for _ in range(ecgs_len):
        test_ecgs.append(ECGImport(**get_single_ecg(total_samples=2)))
    return test_ecgs


def get_single_ecg(total_samples: int = 10):
    return {
        "name": f"User-{create_random_password(4)}",
        "total_samples": total_samples,
        "signal": [1, 2, 3, 4, 5, 6, 7, 8, 9, 0],
        "t_cross_zero": 1,
    }


def test_valid_user(request: Request):
    return {"Authorization": "Bearer some-token"}


@pytest.fixture()
def authenticate_mock_client():
    app = create_api()
    app.dependency_overrides[JWTBearer] = test_valid_user

    return TestClient(app)


@pytest.fixture()
def override_get_db():
    test_db = "postgresql://idoven:idoven@db:5432/test"
    engine = Database(test_db).engine
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def get_test_admin_token():
    payload = signJWT(
        user_email="admin@idoven-challenge.com",
        role=99
    )
    return ["Bearer", payload['access_token']]


@pytest.fixture()
def get_test_standard_token():
    payload = signJWT(
        user_email="user_id@idoven-challenge.com",
        role=0
    )
    return ["Bearer", payload['access_token']]
