from pydantic import EmailStr

from src.types.annotated import PasswordStr
from src.types.base import ImmutableDTO


__all__ = ["SignInRequestDTO"]


class SignInRequestDTO(ImmutableDTO):
    email: EmailStr
    password: PasswordStr
