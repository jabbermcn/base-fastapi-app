from typing import Literal

from src.types.base import ImmutableDTO


class HTTPExceptionModel(ImmutableDTO):
    detail: str = "something_went_wrong"


class UserNotFoundErrorDTO(ImmutableDTO):
    detail: Literal["user_not_found"] = "user_not_found"


class UserAlreadyExistErrorDTO(ImmutableDTO):
    detail: Literal["user_already_exist"] = "user_already_exist"
