from fastapi import HTTPException, status


def ECGUnknownError(error: str):
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={
            "message": f"Unknown Error: {error}"
        }
    )


def ECGWithInvalidData(data: dict):
    """Base Error for
    """
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail={
            "message": "Some ECGs are not valid",
            "data": data
        }
    )


def ECGErrorSavingData():
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={
            "message": "There was an error saving data in the Database"
        }
    )
