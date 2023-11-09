import uuid

# from pydantic import UUID4
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel

from core.utils import camel_to_snake_case


class DBMixin(SQLModel):
    """Mixin for database models."""

    id: uuid.UUID | None = Field(primary_key=True, default_factory=uuid.uuid4)

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return camel_to_snake_case(cls.__name__)
