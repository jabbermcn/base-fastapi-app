from sqlalchemy import TIMESTAMP, Column
from sqlalchemy.orm import declarative_mixin

from src.utils.datetime import now


__all__ = ["LifecycleMixin"]


@declarative_mixin
class LifecycleMixin:
    created_at = Column(
        TIMESTAMP(timezone=True),
        insert_default=now,
        nullable=False,
        comment="Date of created",
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        onupdate=now,
        nullable=True,
        comment="Date of last updated",
    )
