__all__ = [
    "JWTError",
    "DecodeError",
    "JWTStorageUnavailableError",
    "IncorrectJWTBanPayloadError",
]


class JWTError(Exception):
    detail: str = "jwt_error"


class DecodeError(JWTError):
    detail = "jwt_decode"


class JWTStorageUnavailableError(JWTError):
    detail = "jwt_storage_unavailable"


class IncorrectJWTBanPayloadError(JWTError):
    detail = "incorrect_jwt_ban_payload"
