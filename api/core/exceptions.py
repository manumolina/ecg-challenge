from fastapi import HTTPException, status


def BaseUnknownError(error: str):
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={
            "message": f"Unknown Error: {error}",
        },
    )


def BaseErrorSavingData():
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={
            "message": "There was an error saving data in the Database",
        },
    )
