from fastapi import HTTPException, status

from core.exceptions import BaseErrorSavingData, BaseUnknownError, BaseErrorSavingFile


def ECGUnknownError(error: str):
    BaseUnknownError(error)


def ECGErrorSavingFile():
    BaseErrorSavingFile()


def ECGErrorSavingData():
    BaseErrorSavingData()


def ECGWithInvalidData(data: dict):
    """Used if any value from request are not valid."""
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail={
            "message": "Some ECGs are not valid",
            "data": data,
        },
    )
