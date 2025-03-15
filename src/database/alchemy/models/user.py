from uuid import uuid4

from sqlalchemy import UUID, VARCHAR, Column
from sqlalchemy.orm import relationship

from src.database.alchemy.mixins import LifecycleMixin, SoftDeleteMixin
from src.database.alchemy.models.base import Base


__all__ = ["User"]


class User(Base, LifecycleMixin, SoftDeleteMixin):
    """
    User model.

    Represents a registered user in the system.

    :param id: Unique identifier for the user, represented as a UUID.
               The system automatically generates this value for new rows.
    :param email: Email address of the user. Must be unique.
    :param password_hash: Password hash for the user's authentication.
    :param created_at: Timestamp that shows when the user was created.
                       The database sets this value when the user is first saved.
    :param updated_at: Timestamp that shows when the user was last updated.
                       The database updates this value whenever the user changes.
    :param is_deleted: Flag that indicates whether the user is deleted (soft delete) or not.
                       Defaults to False.
    :param deleted_at: Timestamp that shows when the user was soft-deleted.
                       The database sets this value to the current timestamp when the user is marked as deleted.
    """

    id = Column(
        UUID,
        insert_default=uuid4,
        primary_key=True,
    )
    email = Column(
        VARCHAR(length=254),
        nullable=False,
        unique=True,
    )
    password_hash = Column(
        VARCHAR(length=128),
        nullable=True,
    )

    projects = relationship(
        argument="Project",
        back_populates="user",
        uselist=True,
        viewonly=True,
    )

    def __str__(self) -> str:
        return self.email
