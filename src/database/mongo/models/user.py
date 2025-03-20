from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from beanie import Document, Link
from pydantic import EmailStr, Field

from src.database.mongo.models.record import Record
from src.utils.datetime import now


if TYPE_CHECKING:
    from src.database.mongo.models.record import Record

__all__ = ["User"]


class User(Document):
    """
    User model for MongoDB.

    Represents a registered user in the system.

    :param id: Unique identifier for the user (UUID).
    :param email: Email address of the user (unique).
    :param password_hash: Hashed password for authentication.
    :param created_at: Timestamp of when the user was created.
    :param updated_at: Timestamp of last update.
    :param is_deleted: Flag for soft deletion.
    :param deleted_at: Timestamp when the user was softly deleted.
    :param records: List of projects owned by the user.
    """

    id: UUID = Field(default_factory=uuid4)
    email: EmailStr
    password_hash: str | None = Field(None, max_length=128)
    created_at: datetime = Field(default_factory=now)
    updated_at: datetime = Field(default_factory=now)
    is_deleted: bool = Field(default=False)
    deleted_at: datetime | None = None

    records: list[Link["Record"]]

    class Settings:
        name = "user"

    def __str__(self):
        return self.email
