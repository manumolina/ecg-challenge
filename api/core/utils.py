import random
import re
import string

from passlib.context import CryptContext

DEFAULT_PASS_LEN = 32


def camel_to_snake_case(camel_case: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z][^A-Z])", "_", camel_case).lower()


def create_random_password(pass_len: int = DEFAULT_PASS_LEN):
    char_list = ""
    char_list += string.ascii_letters
    char_list += string.digits
    password = []
    for _ in range(pass_len):
        password.append(
            random.choice(char_list),
        )
    return "".join(password)


def hash_string(data: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(data)
