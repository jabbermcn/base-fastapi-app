from collections.abc import Sequence
from typing import Any
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.database.models import Project
from src.exceptions import ObjectNotFoundError, ProjectInternalServerError
from src.repos import ProjectRepo
from src.types import ProjectCreateRequestDTO, ProjectUpdateRequestDTO


__all__ = ["ProjectService"]


class ProjectService:
    def __init__(self, session: AsyncSession):
        self.repo = ProjectRepo(session=session)

    async def get(self, project_id: UUID) -> Project:
        project = await self.repo.get(options=[joinedload(Project.user)], filters=[Project.id == project_id])
        if not project:
            raise ObjectNotFoundError(name="project")
        return project

    async def create(self, user_id: UUID | str, data: ProjectCreateRequestDTO) -> Project:
        project_data = data.model_dump()
        project_data["user_id"] = user_id
        try:
            return await self.repo.create(obj=project_data)
        except IntegrityError:
            raise ProjectInternalServerError()

    async def update(self, project_id: UUID, data: ProjectUpdateRequestDTO) -> Project:
        project = await self.repo.update(_id=project_id, obj=data.model_dump(exclude_unset=True))
        if not project:
            raise ObjectNotFoundError(name="project")
        return project

    async def delete(self, project_id: UUID) -> None:
        if not await self.repo.delete(_id=project_id):
            raise ObjectNotFoundError(name="project")

    async def get_list(
        self,
        page: int,
        page_size: int,
    ) -> Sequence[Project | Any]:
        return await self.repo.get_list(
            page=page,
            page_size=page_size,
            options=[joinedload(Project.user)],
        )

    async def count(self) -> int:
        return await self.repo.count()
