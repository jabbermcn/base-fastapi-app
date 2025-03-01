from math import ceil
from uuid import UUID

from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from api.exception_handlers.factory import ExceptionHandlerFactory
from api.exeptions import (
    FastAPICacheException,
    InternalServerException,
    ObjectExistsException,
    ObjectNotFoundException,
    ServiceResponseValidationException,
)
from src.exceptions import FastAPICacheError, ObjectAlreadyExistError, ObjectNotFoundError
from src.services import ProjectService
from src.types import ProjectCreateRequestDTO, ProjectDTO, ProjectUpdateRequestDTO
from src.types.pagination import Pagination, Paginator
from src.types.project.project import ProjectExtendedDTO


__all__ = ["RESTProjectService"]

project_exception_handler = ExceptionHandlerFactory(
    exc_mapping={
        ValidationError: ServiceResponseValidationException(name="project"),
        ObjectNotFoundError: ObjectNotFoundException(name="project"),
        ObjectAlreadyExistError: ObjectExistsException(name="project"),
        FastAPICacheError: FastAPICacheException(name="project"),
    },
    default_exc=InternalServerException(name="project"),
)


class RESTProjectService:
    def __init__(self, session: AsyncSession):
        self._project_service = ProjectService(session=session)

    @project_exception_handler()
    async def get_project(self, project_id: UUID, user_id: UUID | str) -> ProjectExtendedDTO:
        return ProjectExtendedDTO.model_validate(
            await self._project_service.get(project_id=project_id, user_id=user_id)
        )

    @project_exception_handler()
    async def create_project(self, user_id: UUID | str, data: ProjectCreateRequestDTO) -> ProjectDTO:
        return ProjectDTO.model_validate(await self._project_service.create(data=data, user_id=user_id))

    @project_exception_handler()
    async def delete_project(self, project_id: UUID, user_id: UUID | str) -> None:
        await self._project_service.delete(project_id=project_id, user_id=user_id)

    @project_exception_handler()
    async def update_project(self, project_id: UUID, user_id: UUID | str, data: ProjectUpdateRequestDTO) -> ProjectDTO:
        return ProjectDTO.model_validate(
            await self._project_service.update(project_id=project_id, user_id=user_id, data=data)
        )

    @project_exception_handler()
    async def get_projects(self, user_id: UUID | str, page: int, page_size: int) -> Paginator[ProjectExtendedDTO]:
        return Paginator(
            results=[
                ProjectExtendedDTO.model_validate(project)
                for project in await self._project_service.get_list(user_id=user_id, page=page, page_size=page_size)
            ],
            pagination=Pagination(
                page_size=page_size,
                page=page,
                page_count=ceil(await self._project_service.count(user_id=user_id) / page_size),
            ),
        )
