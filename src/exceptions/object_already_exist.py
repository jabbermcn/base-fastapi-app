from src.exceptions.base import BaseError


__all__ = ["ObjectAlreadyExistError"]


class ObjectAlreadyExistError(BaseError):
    detail = "{name}_already_exists"

    def __init__(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError("Name must be a string")

        if not name:
            raise ValueError("Name cannot be empty")

        self.detail = self.detail.format(name=name)
