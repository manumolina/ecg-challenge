import os

from starlette.testclient import TestClient

from application_factory import create_api
from services.user.routers.user import PATH_PREFIX

app = create_api()
client = TestClient(app)


def test_login_with_wrong_credentials():
    path = os.path.join(PATH_PREFIX, "login")
    response = client.post(
        path,
        json={
            "email": "tester",
            "password": "tester",
        },
    )
    assert response.status_code == 422


def test_login_with_valid_credentials():
    path = os.path.join(PATH_PREFIX, "login")
    response = client.post(
        path,
        json={
            "email": "user_1@idoven-challenge.com",
            "password": "gCPiYzbjE3VrUXYzFLq3TIA0HlScjFdS",
        },
    )
    assert response.status_code == 200


def test_get_user_list_without_token():
    path = PATH_PREFIX
    response = client.get(path, headers=None)
    assert response.status_code == 403


def test_get_user_list_with_token():
    pass


def test_create_new_user_without_token():
    path = PATH_PREFIX
    response = client.post(
        path,
        data={
            "username": "test_idoven",
            "email": "test@idoven-challenge.com",
            "role": "0",
        },
        headers=None,
    )
    assert response.status_code == 403
