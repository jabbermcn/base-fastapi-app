from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT


__all__ = ["ObjectAlreadyExistException", "ObjectNotFoundException"]


class ObjectAlreadyExistException(HTTPException):
    def __init__(self, name: str):
        super().__init__(status_code=HTTP_409_CONFLICT, detail=f"{name}_already_exists")


class ObjectNotFoundException(HTTPException):
    def __init__(self, name: str):
        super().__init__(status_code=HTTP_404_NOT_FOUND, detail=f"{name}_not_found")
