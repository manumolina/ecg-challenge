from datetime import datetime
from core.schemas.base import DBMixin


class User(DBMixin, table=True):
    created: datetime
    updated: datetime
    username: str
    email: str
