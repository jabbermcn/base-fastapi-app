from src.exceptions.base import BaseError


__all__ = ["ObjectNotFoundError"]


class ObjectNotFoundError(BaseError):
    details = "{name}_not_found"

    def __init__(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError("Name must be a string")

        if not name:
            raise ValueError("Name cannot be empty")

        self.details = self.details.format(name=name)
