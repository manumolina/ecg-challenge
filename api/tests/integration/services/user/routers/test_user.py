import os
from application_factory import create_api
from services.user.routers.user import PATH_PREFIX
from unittest.mock import patch

app = create_api()


def test_login_with_wrong_credentials(authenticate_mock_client):
    path = os.path.join(PATH_PREFIX, "login")
    response = authenticate_mock_client.post(
        path,
        json={
            "email": "tester",
            "password": "tester",
        },
    )
    assert response.status_code == 422


def test_login_with_valid_credentials(authenticate_mock_client):
    path = os.path.join(PATH_PREFIX, "login")
    response = authenticate_mock_client.post(
        path,
        json={
            "email": "user_1@idoven-challenge.com",
            "password": "gCPiYzbjE3VrUXYzFLq3TIA0HlScjFdS",
        },
    )
    assert response.status_code == 200


def test_get_user_list_without_token(authenticate_mock_client):
    path = PATH_PREFIX
    response = authenticate_mock_client.get(path, headers=None)
    assert response.status_code == 403


def test_get_user_list_with_standard_token(
    authenticate_mock_client, get_test_standard_token
):
    path = PATH_PREFIX
    response = authenticate_mock_client.get(
        path,
        headers={'Authorization': '{} {}'.format(*get_test_standard_token)}
    )
    expected_error = {'detail': 'Invalid user role. Only administrators allowed.'}
    assert response.status_code == 403
    assert response.json() == expected_error


def test_get_user_list_with_admin_token(
    authenticate_mock_client, get_test_admin_token
):
    path = PATH_PREFIX
    response = authenticate_mock_client.get(
        path,
        headers={'Authorization': '{} {}'.format(*get_test_admin_token)}
    )
    assert response.status_code == 200


def test_create_new_user_without_token(authenticate_mock_client):
    path = PATH_PREFIX
    response = authenticate_mock_client.post(
        path,
        json={
            "username": "test_idoven",
            "email": "test@idoven-challenge.com",
            "role": "0",
        },
    )
    assert response.status_code == 403


def test_create_new_user_with_standard_token(
    authenticate_mock_client, get_test_standard_token
):
    path = PATH_PREFIX
    response = authenticate_mock_client.post(
        path,
        json={
            "username": "test_idoven",
            "email": "test@idoven-challenge.com",
            "role": "0",
        },
        headers={'Authorization': '{} {}'.format(*get_test_standard_token)}
    )
    expected_error = {'detail': 'Invalid user role. Only administrators allowed.'}
    assert response.status_code == 403
    assert response.json() == expected_error


@patch("services.user.logic.user.UserLogic.new")
def test_create_new_user_with_admin_token(
    mock_new_user, authenticate_mock_client, get_test_admin_token
):
    path = PATH_PREFIX
    mock_new_user.return_value = {}
    response = authenticate_mock_client.post(
        path,
        json={
            "username": "test_idoven",
            "email": "test@idoven-challenge.com",
            "role": 0,
        },
        headers={'Authorization': '{} {}'.format(*get_test_admin_token)}
    )
    assert response.status_code == 200
