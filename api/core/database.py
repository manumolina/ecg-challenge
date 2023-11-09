import os
from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy.engine import URL
from sqlmodel import Session, create_engine
from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
