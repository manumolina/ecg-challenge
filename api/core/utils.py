import inspect
import re
from pathlib import Path
from typing import Any


def camel_to_snake_case(camel_case: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z][^A-Z])", "_", camel_case).lower()
