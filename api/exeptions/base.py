from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR


__all__ = ["ObjectExistsException", "ObjectNotFoundException", "InternalServerException", "FastAPICacheException"]


class ObjectExistsException(HTTPException):
    def __init__(self, name: str):
        super().__init__(status_code=HTTP_409_CONFLICT, detail=f"{name}_already_exists")


class ObjectNotFoundException(HTTPException):
    def __init__(self, name: str):
        super().__init__(status_code=HTTP_404_NOT_FOUND, detail=f"{name}_not_found")


class InternalServerException(HTTPException):
    def __init__(self, name: str):
        super().__init__(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"something_went_wrong_with_{name}")


class FastAPICacheException(HTTPException):
    def __init__(self, name: str):
        super().__init__(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"fastapi_cache_clear_error_{name}")
