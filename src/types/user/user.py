from pydantic import UUID4, EmailStr

from src.types.base import ImmutableDTO


__all__ = ["UserDTO"]


class UserDTO(ImmutableDTO):
    id: UUID4
    email: EmailStr
