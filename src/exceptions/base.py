__all__ = ["ObjectAlreadyExistError", "ObjectNotFoundError", "FastAPICacheError"]


class BaseError(Exception):
    detail: str = "something_went_wrong"

    def __str__(self) -> str:
        return self.detail


class ObjectAlreadyExistError(BaseError):
    detail = "{name}_already_exists"

    def __init__(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError("Name must be a string")

        if not name:
            raise ValueError("Name cannot be empty")

        self.detail = self.detail.format(name=name)


class ObjectNotFoundError(BaseError):
    detail = "{name}_not_found"

    def __init__(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError("Name must be a string")

        if not name:
            raise ValueError("Name cannot be empty")

        self.detail = self.detail.format(name=name)


class FastAPICacheError(BaseError):
    detail = "{name}_fastapi_cache_clear"

    def __init__(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError("Name must be a string")

        if not name:
            raise ValueError("Name cannot be empty")

        self.detail = self.detail.format(name=name)
