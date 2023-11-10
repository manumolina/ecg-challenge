from typing import Annotated
from fastapi import APIRouter, Request, Body
from services.ecg.logic.default import ECGLogic
from services.ecg.schemas.ecg import ECGImportList
from services.ecg.exceptions import ECGWithInvalidData

CLASS_TAG = "ECG_API"
ecg_router = APIRouter()


@ecg_router.post("/load")
async def load_ecg_list(
    request: Request,
    ecg_list: Annotated[
        ECGImportList,
        Body(
            examples=[
                {
                    "name": "User-001-ECG-001",
                    "total_samples": 10,
                    "signal": [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
                }
            ],
        ),
    ],
) -> dict:
    """Check HTTP exceptions

    Args:
        request (Request): _description_
        ecg_list (_type_, optional): _description_. Defaults to [ { "name": "User-001-ECG-001", "total_samples": 100, "signal": [1, 2, 3, 4, 5, 6, 7, 8, 9, 0] } ], ), ].

    Returns:
        dict: _description_
    """
    try:
        user_id = "cece5379-495c-4746-ac84-a53d35b37a50"
        result = ECGLogic().load(user_id, ecg_list.data)
        if result["invalid"]["total"]:
            ECGWithInvalidData(result["invalid"])
        return result
    except Exception:
        raise
