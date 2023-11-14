from typing import Annotated

from fastapi import APIRouter, Body, Depends, Request

from core.auth.auth_bearer import JWTBearer
from services.ecg.exceptions import ECGUnknownError, ECGWithInvalidData
from services.ecg.logic.ecg import ECGLogic
from services.ecg.schemas.ecg import ECGImportList

CLASS_TAG = "ECG_API"
PATH_PREFIX = "/sources/ecg"
ecg_router = APIRouter()


@ecg_router.post("/load", dependencies=[Depends(JWTBearer(only_admin=False))])
async def load_ecg_list(
    request: Request,
    ecg_list: Annotated[
        ECGImportList,
        Body(
            examples=[
                {
                    "name": "User-001-ECG-001",
                    "total_samples": 10,
                    "signal": [1, 2, 3, 4, 5, 6, 7, 8, 9, 0],
                },
            ],
        ),
    ],
) -> dict:
    result = ECGLogic(request).load(ecg_list.data)
    try:
        # Not allowed to save data if invalid ecgs are included
        if result["invalid"]["total"]:
            ECGWithInvalidData(result["invalid"])
    except KeyError as e:
        ECGUnknownError(e)
    return result


@ecg_router.get("/", dependencies=[Depends(JWTBearer(only_admin=False))])
async def retrieve_user_ecgs(
    request: Request,
) -> dict:
    result = ECGLogic(request).get_user_ecgs_from_request()
    return {
        "total": len(result),
        "data": result,
    }
