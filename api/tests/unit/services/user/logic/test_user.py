from unittest.mock import patch

from core.auth.auth_handler import decodeJWT
from services.user.logic.user import UserLogic
from services.user.schemas.user import UserImport, UserView


@patch("services.user.data_sources.user.UserData.insert")
def test_new_user_with_valid_data(mock_user_data_insert):
    # Should return a valid User object with a random password
    mock_user_data_insert.return_value = None

    user_test = UserImport(
        username="test",
        email="test@test.com",
        role=0,
    )
    result = UserLogic.new(user_test)
    user_test_keys = list(user_test.__dict__.keys())
    assert list(result.keys()) == user_test_keys


@patch("services.user.data_sources.user.UserData.get")
def test_get_all_with_list_of_users(mock_user_data_get, get_list_of_users):
    test_users = get_list_of_users
    mock_user_data_get.return_value = test_users
    result = UserLogic.get_all()
    assert all(type(user) is UserView for user in result)
    assert len(result) == len(test_users)


@patch("services.user.data_sources.user.UserData.get")
def test_get_user_id_from_existing_email(mock_user_data_get, get_single_user):
    valid_email = get_single_user.email
    mock_user_data_get.return_value = [get_single_user]
    user_id = UserLogic.get_user_id_from_email(valid_email)
    assert user_id == get_single_user.id


@patch("services.user.data_sources.user.UserData.get")
def test_get_user_id_from_non_existing_email(mock_user_data_get):
    valid_email = "fake@email.com"
    mock_user_data_get.return_value = None
    user_id = UserLogic.get_user_id_from_email(valid_email)
    assert user_id is None


@patch("services.user.data_sources.user.UserData.validate_password_by_email")
def test_check_user_from_existing_email(
    mock_user_data_validate_pass, get_single_user,
):
    mock_user_data_validate_pass.return_value = get_single_user.__dict__
    token = UserLogic.check_user(get_single_user)
    token_decoded = decodeJWT(token["access_token"])

    assert "access_token" in token
    assert token_decoded["user_email"] == get_single_user.email
    assert token_decoded["role"] == get_single_user.role


@patch("services.user.data_sources.user.UserData.validate_password_by_email")
def test_check_user_from_non_existing_email(
    mock_user_data_validate_pass, get_single_user,
):
    mock_user_data_validate_pass.return_value = None
    token = UserLogic.check_user(get_single_user)
    assert token is None


@patch("services.user.data_sources.user.UserData.validate_user_has_role_by_email")
def test_user_has_role_from_existing_email_and_role(
    mock_user_data_validate_role, get_single_user,
):
    # Not necessary to test here. No logic inside UserData method
    mock_user_data_validate_role.return_value = None
    _ = UserLogic.user_has_role(get_single_user.email, get_single_user.role)
    assert True
