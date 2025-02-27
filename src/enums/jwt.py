from enum import StrEnum, auto, unique


__all__ = ["JWTPrefix"]


@unique
class JWTPrefix(StrEnum):
    SUB = auto()
    JTI = auto()
