import uuid

from pydantic import BaseModel
from typing import Optional
from sqlmodel import Field

from core.schemas.base import DBMixin


class ECG(DBMixin, table=True):
    date: str
    user: str  # = Field(default=None, foreign_key="user.id")


class ECGLead(DBMixin, table=True):
    ecg_id: uuid.UUID = Field(default=None, foreign_key="ecg.id")
    name: str
    total_samples: int
    signal: list[int]


class ECGImport(BaseModel):
    name: str
    total_samples: Optional[int]
    signal: list[int]


class ECGImportList(BaseModel):
    data: list[ECGImport]
