from typing import Annotated
from fastapi import APIRouter, Request, Body
from services.ecg.logic.default import ECGLogic
from services.ecg.schemas.ecg import ECGImportList
from services.ecg.exceptions import ECGWithInvalidData, ECGUnknownError

CLASS_TAG = "ECG_API"
PATH_PREFIX = "/sources/ecg"
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
    user_id = "cece5379-495c-4746-ac84-a53d35b37a50"
    result = ECGLogic().load(user_id, ecg_list.data)
    try:
        # Not allowed to save data if invalid ecgs are included
        if result["invalid"]["total"]:
            ECGWithInvalidData(result["invalid"])
    except KeyError as e:
        ECGUnknownError(e)
    return result


@ecg_router.get("/")
async def retrieve_user_ecgs(
    request: Request,
) -> dict:
    user_id = "cece5379-495c-4746-ac84-a53d35b37a50"
    result = ECGLogic().get_user_ecgs(user_id)
    return {
        "total": len(result),
        "data": result
    }
