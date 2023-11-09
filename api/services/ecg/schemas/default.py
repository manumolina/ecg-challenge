import uuid
from core.schemas.base import DBMixin
from sqlmodel import SQLModel, Field, CheckConstraint, Column, Integer


class ECG(DBMixin, table=True):
    date: str


class ECGLead(DBMixin, table=True):
    ecg_id: uuid.UUID
    name: str
    total_samples: int
    signal: str


# class ECG(SongBase):
#     pass

# class SongCreate(SongBase):
#     pass
