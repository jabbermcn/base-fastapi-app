from pydantic import UUID4, EmailStr

from src.types.base import ImmutableDTO


__all__ = ["UserDTO", "UserCreateDTO", "UserUpdateDTO"]


class UserDTO(ImmutableDTO):
    id: UUID4
    email: EmailStr


class UserCreateDTO(ImmutableDTO):
    email: EmailStr


class UserUpdateDTO(ImmutableDTO):
    email: EmailStr
