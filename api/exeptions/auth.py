from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN


__all__ = ["TokenNotProvidedException", "IncorrectPasswordException", "InvalidTokenOrExpiredException"]


class TokenNotProvidedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=HTTP_403_FORBIDDEN, detail="token_not_provided")


class InvalidTokenOrExpiredException(HTTPException):
    def __init__(self):
        super().__init__(status_code=HTTP_403_FORBIDDEN, detail="invalid_token_or_expired")


class IncorrectPasswordException(HTTPException):
    def __init__(self):
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail="incorrect_password")
