from enum import StrEnum, auto, unique


__all__ = ["ProjectType"]


@unique
class ProjectType(StrEnum):
    TYPE1 = auto()
    TYPE2 = auto()
