from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from sqlmodel import ARRAY, Column, Field, Integer

from core.schemas.base import DBMixin


class ECG(DBMixin, table=True):
    created: datetime = Field(default_factory=datetime.now)
    user: UUID = Field(default=None, foreign_key="user.id")


class ECGLead(DBMixin, table=True):
    ecg_id: UUID = Field(default=None, foreign_key="ecg.id")
    name: str
    total_samples: int
    signal: list = Field(default_factory=list, sa_column=Column(ARRAY(Integer)))
    t_cross_zero: int


class ECGImport(BaseModel):
    name: str
    total_samples: int | None
    signal: list[int]


class ECGImportList(BaseModel):
    data: list[ECGImport]


class ECGOutput(BaseModel):
    name: str
    total_samples: int
    signal: list
    t_cross_zero: int
