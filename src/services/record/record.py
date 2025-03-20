from collections.abc import Sequence
from uuid import UUID

from fastapi_cache import FastAPICache

from src.database.mongo.models import Record
from src.exceptions import FastAPICacheError, InternalServerError, ObjectNotFoundError
from src.repos.mongo.record import RecordRepo
from src.types.record import RecordCreateRequestDTO, RecordUpdateRequestDTO


__all__ = ["RecordService"]


class RecordService:
    def __init__(self, repo: RecordRepo):
        self.repo = repo

    async def get(self, record_id: UUID | str, user_id: UUID | str) -> Record:
        record = await self.repo.get(filters={"_id": record_id, "user": user_id})
        if not record:
            raise ObjectNotFoundError(name="record")
        return record

    async def create(self, user_id: UUID | str, data: RecordCreateRequestDTO) -> Record:
        record_data = data.model_dump()
        record_data["user"] = user_id
        try:
            await FastAPICache.clear(namespace="record")
            return await self.repo.create(record_data)
        except Exception:
            raise InternalServerError(name="record")

    async def update(self, record_id: UUID | str, data: RecordUpdateRequestDTO) -> Record:
        try:
            await FastAPICache.clear(namespace="record")
        except Exception:
            raise FastAPICacheError(name="record")
        record = await self.repo.update(_id=record_id, obj=data.model_dump(exclude_unset=True))
        if not record:
            raise ObjectNotFoundError(name="record")
        return record

    async def delete(self, record_id: UUID | str) -> None:
        try:
            await FastAPICache.clear(namespace="record")
        except Exception:
            raise FastAPICacheError(name="record")
        record = await self.repo.delete(_id=record_id)
        if not record:
            raise ObjectNotFoundError(name="record")

    async def get_list(
        self,
        user_id: UUID | str,
        page: int,
        page_size: int,
    ) -> Sequence[Record]:
        return await self.repo.get_list(page=page, page_size=page_size, filters={"user_id": user_id})

    async def count(self, user_id: UUID | str) -> int:
        return await self.repo.count(filters={"user_id": user_id})
