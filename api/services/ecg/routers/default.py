from typing import Annotated
from fastapi import APIRouter, Request, Body
from services.ecg.logic.default import ECGLogic
from services.ecg.schemas.default import ECGImportList

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
                    "total_samples": 100,
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
        result = ECGLogic.load(ecg_list.data)
        return {"message": "Loaded!"}
    except Exception:
        raise
