from math import ceil
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from api.exeptions import InternalServerException, ObjectExistsException, ObjectNotFoundException
from src.exceptions import ObjectAlreadyExistError, ObjectNotFoundError, ProjectInternalServerError
from src.services import ProjectService
from src.types import ProjectCreateRequestDTO, ProjectDTO, ProjectUpdateRequestDTO
from src.types.pagination import Pagination, Paginator
from src.types.project.project import ProjectExtendedDTO


__all__ = ["RESTProjectService"]


class RESTProjectService:
    def __init__(self, session: AsyncSession):
        self._project_service = ProjectService(session=session)

    async def get_project(self, project_id: UUID) -> ProjectExtendedDTO:
        try:
            return ProjectExtendedDTO.model_validate(await self._project_service.get(project_id=project_id))
        except ProjectInternalServerError:
            raise InternalServerException(name="project")

    async def create_project(self, user_id: UUID | str, data: ProjectCreateRequestDTO) -> ProjectDTO:
        try:
            return ProjectDTO.model_validate(await self._project_service.create(data=data, user_id=user_id))
        except ObjectAlreadyExistError:
            raise ObjectExistsException(name="project")

    async def delete_project(self, project_id: UUID) -> None:
        try:
            await self._project_service.delete(project_id=project_id)
        except ObjectNotFoundError:
            raise ObjectNotFoundException(name="project")

    async def update_project(self, project_id: UUID, data: ProjectUpdateRequestDTO) -> ProjectDTO:
        try:
            return ProjectDTO.model_validate(await self._project_service.update(project_id=project_id, data=data))
        except ObjectNotFoundError:
            raise ObjectNotFoundException(name="project")

    async def get_projects(self, page: int, page_size: int) -> Paginator[ProjectExtendedDTO]:
        return Paginator(
            results=[
                ProjectExtendedDTO.model_validate(project)
                for project in await self._project_service.get_list(page=page, page_size=page_size)
            ],
            pagination=Pagination(
                page_size=page_size,
                page=page,
                page_count=ceil(await self._project_service.count() / page_size),
            ),
        )
