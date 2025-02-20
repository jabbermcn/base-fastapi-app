from uuid import uuid4

from sqlalchemy import UUID, Column

from src.database.mixins import LifecycleMixin, SoftDeleteMixin
from src.database.models.base import Base


__all__ = ["User"]


class User(Base, LifecycleMixin, SoftDeleteMixin):
    """
    User model.

    Represents a registered user in the system.

    :param id: Unique identifier for the user, represented as a UUID.
               The system automatically generates this value for new rows.
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
