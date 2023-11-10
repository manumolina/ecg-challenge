import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from sqlmodel import Field, Column, ARRAY, Integer

from core.schemas.base import DBMixin


class ECG(DBMixin, table=True):
    created: datetime = Field(default_factory=datetime.now,)
    user: uuid.UUID = Field(default=None, foreign_key="user.id")


class ECGLead(DBMixin, table=True):
    ecg_id: uuid.UUID = Field(default=None, foreign_key="ecg.id")
    name: str
    total_samples: int
    signal: list = Field(default_factory=list, sa_column=Column(ARRAY(Integer)))
    t_cross_zero: int


class ECGImport(BaseModel):
    name: str
    total_samples: Optional[int]
    signal: list[int]


class ECGImportList(BaseModel):
    data: list[ECGImport]


class ECGOutput(BaseModel):
    name: str
    total_samples: int
    signal: list
    t_cross_zero: int
