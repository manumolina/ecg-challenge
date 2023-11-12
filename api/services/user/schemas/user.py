from datetime import datetime
from pydantic import BaseModel, EmailStr
from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from core.schemas.base import DBMixin


class User(DBMixin, table=True):
    __table_args__ = (UniqueConstraint("email"),)
    created: datetime = Field(default_factory=datetime.now,)
    updated: datetime = Field(default_factory=datetime.now,)
    username: str
    email: str
    password: str
    disabled: bool = 0
    role: int = 0  # (0) read + write, (99) admin


class UserImport(BaseModel):
    username: str
    email: EmailStr = Field(...)
    role: int = 0

    class Config:
        schema_extra = {
            "example": {
                "username": "test_idoven",
                "email": "test@idoven-challenge.com",
                "role": "0"
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "test@idoven-challenge.com",
                "password": "idovenpassword"
            }
        }


class UserView(BaseModel):
    username: str
    email: str
    disabled: bool = 0
    role: int = 0  # (0) read + write, (99) admin
