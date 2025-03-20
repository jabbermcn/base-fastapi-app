from abc import ABC
from collections.abc import Sequence
from typing import Any, Generic, TypeVar
from uuid import UUID

from beanie import Document, SortDirection


ModelType = TypeVar("ModelType", bound=Document)


class BaseMongoRepo(ABC, Generic[ModelType]):
    def __init__(self, model: type[ModelType]):
        self._model = model

    async def create(self, obj: dict) -> ModelType:
        document = self._model(**obj)
        await document.insert()
        return document

    async def get(self, filters: dict[str, Any]) -> ModelType | None:
        return await self._model.find_one(filters=filters)

    async def update(self, _id: UUID | str, obj: dict) -> ModelType | None:
        document = await self._model.get(document_id=_id)
        if document:
            await document.update({"$set": obj})
        return document

    async def delete(self, _id: UUID | str) -> ModelType | None:
        document = await self._model.get(document_id=_id)
        if document:
            await document.delete()
        return document

    async def get_list(
        self,
        page: int,
        page_size: int,
        filters: dict[str, Any] | None = None,
        sort: str | tuple[str, SortDirection] | list[tuple[str, SortDirection]] | None = None,
    ) -> Sequence[ModelType]:
        statement = self._model.find(filters or {})
        if sort:
            statement = statement.sort(sort)
        return await statement.skip((page - 1) * page_size).limit(page_size).to_list()

    async def count(self, filters: dict[str, Any] | None = None) -> int:
        return await self._model.find(filters or {}).count()
