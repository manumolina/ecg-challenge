from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from core.schemas.base import DBMixin


class User(DBMixin, table=True):
    __table_args__ = (UniqueConstraint("email"),)
    created: datetime = Field(default_factory=datetime.now,)
    updated: datetime = Field(default_factory=datetime.now,)
    username: str
    email: str
    role: int = 0  # 0 - read, 1 - read + write, 99 - admin


class UserImport(BaseModel):
    username: str
    email: str
