import os
from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy.engine import URL
from sqlmodel import Session, create_engine
from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = os.environ.get("DATABASE_URL")


class Database:
    def __init__(self) -> None:
        self.engine = create_engine(DATABASE_URL, echo=True)

    def init_db(self):
        SQLModel.metadata.create_all(self.engine)

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        db = None
        try:
            db = Session(self.engine)
            yield db
        finally:
            db.close()


database = Database()
