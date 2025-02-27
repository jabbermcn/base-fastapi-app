from datetime import datetime
from typing import TypedDict

from src.types.annotated import JWTStr
from src.types.base import ImmutableDTO


__all__ = ["TokenPairDTO", "TokenPayload"]


class TokenPairDTO(ImmutableDTO):
    access_token: JWTStr
    refresh_token: JWTStr


class TokenPayload(TypedDict):
    sub: str
    iat: datetime | float
    exp: datetime | float
    jti: str
