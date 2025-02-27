from pydantic import EmailStr

from src.types.annotated import PasswordStr
from src.types.base import ImmutableDTO


__all__ = ["SignUpRequestDTO"]


class SignUpRequestDTO(ImmutableDTO):
    email: EmailStr
    password: PasswordStr
