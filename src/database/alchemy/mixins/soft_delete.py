from sqlalchemy import BOOLEAN, TIMESTAMP, Column
from sqlalchemy.orm import declarative_mixin


__all__ = ["SoftDeleteMixin"]


@declarative_mixin
class SoftDeleteMixin:
    is_deleted = Column(BOOLEAN, default=False, server_default="false")
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True, comment="Date of deletion")
