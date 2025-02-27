from src.exceptions.base import BaseError


__all__ = ["IncorrectPasswordError", "TokenIsBannedError"]


class IncorrectPasswordError(BaseError):
    detail = "incorrect_password"


class TokenIsBannedError(BaseError):
    detail = "token_is_banned"
