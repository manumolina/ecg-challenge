from typing import Annotated

from fastapi import APIRouter, Body, Depends, Request
from fastapi import UploadFile, File # HTTPException, status

from core.auth.auth_bearer import JWTBearer
from libs.utils import timer
from services.ecg.exceptions import ECGUnknownError, ECGWithInvalidData
from services.ecg.logic.ecg import ECGLogic
from services.ecg.schemas.ecg import ECGImportList

CLASS_TAG = "ECG_API"
PATH_PREFIX = "/sources/ecg"
ecg_router = APIRouter()


@ecg_router.post("/load/list", dependencies=[Depends(JWTBearer(only_admin=False))])
@timer
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
    result = ECGLogic(request).load_list(ecg_list.data)
    try:
        # Not allowed to save data if invalid ecgs are included
        if result["invalid"]["total"]:
            ECGWithInvalidData(result["invalid"])
    except KeyError as e:
        ECGUnknownError(e)
    return result


@ecg_router.post("/load/file", dependencies=[Depends(JWTBearer(only_admin=False))])
@timer
async def upload(
    request: Request,
    store: bool = False,
    uploaded_file: UploadFile = File(...),
):
    if not uploaded_file.filename:
        ECGUnknownError("File is missing")

    ecg = ECGLogic(request)
    result = ecg.load_file(uploaded_file)
    if not result["status"]:
        ECGUnknownError(result["message"])

    if store:
        ecg.store_file(uploaded_file)

    return {
        "message": "Successfuly uploaded",
        "file": uploaded_file.filename,
        "content": uploaded_file.content_type,
        "size": uploaded_file.size,
    }


@ecg_router.get("/", dependencies=[Depends(JWTBearer(only_admin=False))])
@timer
async def retrieve_user_ecgs(
    request: Request,
) -> dict:
    result = ECGLogic(request).get_user_ecgs_from_request()
    return {
        "total": len(result),
        "data": result,
    }
