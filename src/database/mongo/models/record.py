from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from beanie import BackLink, Document
from pydantic import Field


if TYPE_CHECKING:
    from src.database.mongo.models.user import User

__all__ = ["Record"]


class Record(Document):
    """
    Project model for MongoDB.

    Represents a project created by a user.

    :param id: Unique identifier for the record, represented as a UUID.
               Automatically generated for new documents.
    :param user: Reference to the user who owns the record.
    :param title: The title of the record. Must be at least 1 character long.
    """

    id: UUID = Field(default_factory=uuid4)
    user: BackLink["User"] = Field(original_field="records")  # noqa
    title: str = Field(..., min_length=1, max_length=32)

    class Settings:
        name = "record"

    def __str__(self):
        return self.title
