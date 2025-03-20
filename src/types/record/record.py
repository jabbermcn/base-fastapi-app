from pydantic import UUID4

from src.types.base import ImmutableDTO
from src.types.user.user import UserDTO


__all__ = [
    "RecordCreateRequestDTO",
    "RecordUpdateRequestDTO",
    "RecordDTO",
    "RecordExtendedDTO",
]


class RecordDTO(ImmutableDTO):
    id: UUID4
    title: str


class RecordExtendedDTO(RecordDTO):
    user: UserDTO


class RecordCreateRequestDTO(ImmutableDTO):
    title: str


class RecordUpdateRequestDTO(ImmutableDTO):
    title: str
