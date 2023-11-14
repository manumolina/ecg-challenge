from unittest.mock import patch

from application_factory import create_api
from services.ecg.routers.ecg import PATH_PREFIX

app = create_api()


def test_retrieve_user_ecgs_without_auth(authenticate_mock_client):
    path = PATH_PREFIX
    response = authenticate_mock_client.get(path, headers=None)
    assert response.status_code == 403


def test_retrieve_user_ecgs_with_admin_auth(
    authenticate_mock_client, get_test_admin_token,
):
    path = PATH_PREFIX
    response = authenticate_mock_client.get(
        path,
        headers={"Authorization": "{} {}".format(*get_test_admin_token)},
    )
    expected_error = {"detail": "Invalid user role. Not allowed to administrators."}
    assert response.status_code == 403
    assert response.json() == expected_error


@patch("services.ecg.logic.ecg.ECGLogic.get_user_ecgs_from_request")
def test_retrieve_user_ecgs_with_standard_auth(
    mock_get_user_ecgs_from_request, authenticate_mock_client, get_test_standard_token,
):
    mock_get_user_ecgs_from_request.return_value = []
    path = PATH_PREFIX
    response = authenticate_mock_client.get(
        path,
        headers={"Authorization": "{} {}".format(*get_test_standard_token)},
    )
    assert response.status_code == 200
