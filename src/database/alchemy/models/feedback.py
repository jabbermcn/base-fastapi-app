from uuid import uuid4

from sqlalchemy import BOOLEAN, UUID, VARCHAR, Column

from src.database.alchemy.mixins import LifecycleMixin
from src.database.alchemy.models.base import Base


__all__ = ["Feedback"]


class Feedback(Base, LifecycleMixin):
    """
    Feedback model.

    Represents feedback provided by a user in the system.

    :param id: Unique identifier for the feedback, represented as a UUID.
               Automatically generated for new rows.
    :param email: The email address of the user providing the feedback.
    :param name: The name of the user providing the feedback.
    :param comment: The content of the feedback, with a maximum length of 500 characters.
    :param created_at: Timestamp that shows when the feedback was created.
                       The database sets this value when the feedback is first saved.
    :param updated_at: Timestamp that shows when the feedback was last updated.
                       The database updates this value whenever the feedback changes.
    :param is_processed: Flag indicating whether the feedback has been processed or not.
    """

    id = Column(
        UUID,
        insert_default=uuid4,
        primary_key=True,
    )
    email = Column(
        VARCHAR(length=254),
        nullable=False,
        unique=False,
    )
    name = Column(
        VARCHAR(length=50),
        nullable=False,
        unique=False,
    )
    comment = Column(
        VARCHAR(length=500),
        nullable=False,
        unique=False,
    )
    is_processed = Column(
        BOOLEAN,
        nullable=False,
        default=False,
    )

    def __str__(self) -> str:
        return self.name
