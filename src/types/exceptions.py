from typing import Literal

from src.types.base import ImmutableDTO


class HTTPExceptionModel(ImmutableDTO):
    detail: str


class UserNotFoundErrorDTO(ImmutableDTO):
    detail: Literal["user_not_found"] = "user_not_found"
