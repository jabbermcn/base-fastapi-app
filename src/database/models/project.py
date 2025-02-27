from uuid import uuid4

from sqlalchemy import UUID, VARCHAR, CheckConstraint, Column, Enum, ForeignKey
from sqlalchemy.orm import relationship

from src.database.mixins import LifecycleMixin
from src.database.models.base import Base
from src.enums import ProjectType


__all__ = ["Project"]


class Project(Base, LifecycleMixin):
    """
    Project model.

    Represents a project created by a user.

    :param id: Unique identifier for the project, represented as a UUID.
               Automatically generated for new rows.
    :param user_id: The ID of the user who owns the project. References the user table.
    :param name: The name of the project. Must be at least 1 character long.
    :param type: The type of the project. Defined by the ProjectType enum.
    """

    __table_args__ = (CheckConstraint(sqltext="length(name) >= 1", name="name_min_length"),)

    id = Column(
        UUID,
        insert_default=uuid4,
        primary_key=True,
        index=True,
    )
    user_id = Column(
        UUID,
        ForeignKey(column="user.id", ondelete="CASCADE", onupdate="CASCADE"),
        index=True,
        nullable=False,
        unique=False,
    )
    name = Column(
        VARCHAR(length=32),
        nullable=False,
        unique=False,
    )
    type = Column(Enum(ProjectType), nullable=False, insert_default=ProjectType.TYPE1)

    user = relationship(
        argument="User",
        back_populates="projects",
        uselist=False,
        viewonly=True,
    )

    def __str__(self):
        return self.name
