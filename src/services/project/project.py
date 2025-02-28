from collections.abc import Sequence
from typing import Any
from uuid import UUID

from fastapi_cache import FastAPICache
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.database.models import Project
from src.exceptions import FastAPICacheError, ObjectNotFoundError, ProjectInternalServerError
from src.repos import ProjectRepo
from src.types import ProjectCreateRequestDTO, ProjectUpdateRequestDTO


__all__ = ["ProjectService"]


class ProjectService:
    def __init__(self, session: AsyncSession):
        self.repo = ProjectRepo(session=session)

    async def get(self, project_id: UUID, user_id: UUID | str) -> Project:
        project = await self.repo.get(
            options=[joinedload(Project.user)], filters=[Project.id == project_id, Project.user_id == user_id]
        )
        if not project:
            raise ObjectNotFoundError(name="project")
        return project

    async def create(self, user_id: UUID | str, data: ProjectCreateRequestDTO) -> Project:
        project_data = data.model_dump()
        project_data["user_id"] = user_id
        try:
            await FastAPICache.clear(namespace="project")
            return await self.repo.create(obj=project_data)
        except IntegrityError:
            raise ProjectInternalServerError()
        except Exception:
            raise FastAPICacheError(name="project")

    async def update(self, project_id: UUID, user_id: UUID | str, data: ProjectUpdateRequestDTO) -> Project:
        try:
            await FastAPICache.clear(namespace="project")
        except Exception:
            raise FastAPICacheError(name="project")
        project = await self.repo.update(
            obj=data.model_dump(exclude_unset=True), filters=[Project.id == project_id, Project.user_id == user_id]
        )
        if not project:
            raise ObjectNotFoundError(name="project")
        return project

    async def delete(self, project_id: UUID, user_id: UUID | str) -> None:
        try:
            await FastAPICache.clear(namespace="project")
        except Exception:
            raise FastAPICacheError(name="project")
        if not await self.repo.delete(filters=[Project.id == project_id, Project.user_id == user_id]):
            raise ObjectNotFoundError(name="project")

    async def get_list(
        self,
        user_id: UUID | str,
        page: int,
        page_size: int,
    ) -> Sequence[Project | Any]:
        return await self.repo.get_list(
            page=page, page_size=page_size, options=[joinedload(Project.user)], filters=[Project.user_id == user_id]
        )

    async def count(
        self,
        user_id: UUID | str,
    ) -> int:
        return await self.repo.count(filters=[Project.user_id == user_id])
