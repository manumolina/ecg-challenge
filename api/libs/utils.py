import time
from functools import wraps

from libs.logger import logger


def timer(func):
    # Prints the execution time for the decorated function
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        logger.debug(f"{func.__name__} ran in {round(end - start, 2)}s")
        return result

    return wrapper
