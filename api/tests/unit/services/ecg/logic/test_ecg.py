from unittest.mock import patch
from uuid import uuid4

from services.ecg.logic.ecg import ECGLogic


@patch("services.ecg.data_sources.ecg.ECGData.insert")
@patch("services.user.logic.user.UserLogic.get_user_id_from_request")
def test_load_with_valid_data(
    mock_request,
    mock_ecg_insert,
    authenticate_mock_client,
    get_list_of_valid_ecgs,
):
    mock_request.return_value = uuid4()
    mock_ecg_insert.return_value = None

    test_ecgs = get_list_of_valid_ecgs
    result = ECGLogic(authenticate_mock_client).load(test_ecgs)

    expected_result = {
        "inserted": len(test_ecgs),
        "valid": len(test_ecgs),
        "invalid": {"total": 0, "data": []},
    }
    assert result == expected_result


@patch("services.ecg.data_sources.ecg.ECGData.insert")
@patch("services.user.logic.user.UserLogic.get_user_id_from_request")
def test_load_with_one_invalid_data(
    mock_request,
    mock_ecg_insert,
    authenticate_mock_client,
    get_list_of_invalid_ecgs,
):
    mock_request.return_value = uuid4()
    mock_ecg_insert.return_value = None

    test_ecgs = get_list_of_invalid_ecgs
    result = ECGLogic(authenticate_mock_client).load(test_ecgs)

    assert result["inserted"] != len(test_ecgs)
    assert result["invalid"]["total"] > 0
    assert result["inserted"] + result["invalid"]["total"] == len(test_ecgs)


@patch("services.ecg.data_sources.ecg.ECGData.insert")
@patch("services.user.logic.user.UserLogic.get_user_id_from_request")
def test_save_with_invalid_data(
    mock_request,
    mock_ecg_insert,
    authenticate_mock_client,
    get_list_of_invalid_ecgs,
):
    mock_request.return_value = uuid4()
    mock_ecg_insert.return_value = None

    test_ecg = {
        "user_id": uuid4(),
        "valid_ecgs": [],
        "invalid_ecgs": get_list_of_invalid_ecgs,
    }
    result = ECGLogic(authenticate_mock_client).save(**test_ecg)
    assert result["inserted"] == 0
    assert result["invalid"]["total"] == len(get_list_of_invalid_ecgs)
    assert result["invalid"]["data"] == get_list_of_invalid_ecgs


@patch("services.ecg.data_sources.ecg.ECGData.insert")
@patch("services.user.logic.user.UserLogic.get_user_id_from_request")
def test_save_with_valid_data(
    mock_request,
    mock_ecg_insert,
    authenticate_mock_client,
    get_list_of_valid_ecgs,
):
    mock_request.return_value = uuid4()
    mock_ecg_insert.return_value = None

    test_ecg = {
        "user_id": uuid4(),
        "valid_ecgs": get_list_of_valid_ecgs,
        "invalid_ecgs": [],
    }
    result = ECGLogic(authenticate_mock_client).save(**test_ecg)
    assert result["inserted"] == len(get_list_of_valid_ecgs)
    assert result["invalid"]["total"] == 0


@patch("services.ecg.data_sources.ecg.ECGData.get")
@patch("services.user.logic.user.UserLogic.get_user_id_from_request")
def test_get_user_ecgs_from_request_with_data(
    mock_request,
    mock_ecg_get,
    authenticate_mock_client,
    get_list_of_valid_ecgs_output,
):
    mock_request.return_value = uuid4()
    mock_ecg_get.return_value = [
        ("", ecg) for ecg in get_list_of_valid_ecgs_output
    ]
    result = ECGLogic(authenticate_mock_client).get_user_ecgs_from_request()
    assert len(result) == len(get_list_of_valid_ecgs_output)


@patch("services.ecg.data_sources.ecg.ECGData.get")
@patch("services.user.logic.user.UserLogic.get_user_id_from_request")
def test_get_user_ecgs_from_request_without_data(
    mock_request,
    mock_ecg_get,
    authenticate_mock_client,
):
    mock_request.return_value = uuid4()
    mock_ecg_get.return_value = []
    result = ECGLogic(authenticate_mock_client).get_user_ecgs_from_request()
    assert len(result) == 0


@patch("services.user.logic.user.UserLogic.get_user_id_from_request")
def test_total_number_crossing_signal(mock_request, authenticate_mock_client):
    mock_request.return_value = uuid4()

    dataset = [
        {"signal": [1, 2, 3, 2], "to_find": 0, "result": 0},
        {"signal": [1, 2, 3, 2], "to_find": 1, "result": 1},
        {"signal": [1, 2, 3, 2], "to_find": 2, "result": 2},
    ]
    for data in dataset:
        result = ECGLogic(authenticate_mock_client).total_number_crossing_signal(
            data["signal"], data["to_find"],
        )
        assert result == data["result"]

    # check second parameter not provided
    result = ECGLogic(authenticate_mock_client).total_number_crossing_signal(
        dataset[0]["signal"],
    )
    assert result == dataset[0]["result"]
