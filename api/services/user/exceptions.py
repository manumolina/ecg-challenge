from fastapi import HTTPException, status

from core.exceptions import BaseErrorSavingData, BaseUnknownError


def UserUnknownError(error: str):
    BaseUnknownError(error)


def UserErrorSavingData():
    BaseErrorSavingData()


def UserErrorSignIn():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "message": "Invalid Login",
            "data": {},
        },
    )
