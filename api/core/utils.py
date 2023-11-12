import string
import random
import re
from passlib.context import CryptContext

DEFAULT_PASS_LEN = 32


def camel_to_snake_case(camel_case: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z][^A-Z])", "_", camel_case).lower()


def create_random_password(pass_len: int = DEFAULT_PASS_LEN):
    characterList = ""
    characterList += string.ascii_letters
    characterList += string.digits
    # characterList += string.punctuation
    password = []
    for i in range(pass_len):
        password.append(
            random.choice(characterList)
        )
    return "".join(password)


def hash_string(data: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(data)
