from unittest.mock import patch
from services.user.data_sources.user import UserData


@patch("services.user.data_sources.user.database")
def test_user_insert_with_valid_data(
    mock_db, override_get_db, get_list_of_new_users
):
    mock_db.return_value = override_get_db
    for user in get_list_of_new_users:
        UserData.insert(user)
    assert True
