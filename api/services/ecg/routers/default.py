import uuid
from fastapi import APIRouter
from services.ecg.schemas.default import ECG

CLASS_TAG = "ECG_API"
ecg_router = APIRouter()


@ecg_router.post("/load")
async def load_ecg_list():
    ecg = {"id": uuid.uuid4(), "date": "test2"}
    print(ECG(**ecg))
    return {"message": "Done!"}
