from pydantic import UUID4

from src.enums import ProjectType
from src.types.base import ImmutableDTO
from src.types.user.user import UserDTO


__all__ = ["ProjectDTO", "ProjectCreateRequestDTO", "ProjectUpdateRequestDTO", "ProjectExtendedDTO"]


class ProjectDTO(ImmutableDTO):
    id: UUID4
    name: str
    type: ProjectType


class ProjectExtendedDTO(ProjectDTO):
    user: UserDTO


class ProjectCreateRequestDTO(ImmutableDTO):
    name: str
    type: ProjectType | None


class ProjectUpdateRequestDTO(ImmutableDTO):
    name: str
