import os
from collections.abc import Generator
from contextlib import contextmanager

from sqlmodel import Session, create_engine, SQLModel

DATABASE_URL = os.environ.get("DATABASE_URL")


class Database:
    def __init__(self, db_url: str = DATABASE_URL) -> None:
        self.engine = create_engine(db_url, echo=True)

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
