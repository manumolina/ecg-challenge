from fastapi import HTTPException, status


def BaseUnknownError(error: str):
    # To use when something wrong happen and we don't know what to do with it
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={
            "message": f"Unknown Error: {error}",
        },
    )


def BaseErrorReadingFile():
    # To use when something wrong happen reading a file
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={
            "message": "There was an error reading file",
        },
    )


def BaseErrorSavingFile():
    # To use when something happen storing file locally
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={
            "message": "There was an error storing file",
        },
    )

def BaseErrorSavingData():
    # To use when something happen storing data in the database
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={
            "message": "There was an error saving data in the Database",
        },
    )
