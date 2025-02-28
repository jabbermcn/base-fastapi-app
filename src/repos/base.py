from abc import ABC
from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from sqlalchemy import and_, delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class BaseRepo(ABC, Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: type[ModelType]):
        self._session = session
        self._model = model

    async def create(self, obj: dict) -> ModelType:
        result = await self._session.execute(statement=insert(self._model).values(**obj).returning(self._model))
        await self._session.commit()
        return result.scalar_one_or_none()

    async def get(self, filters: list[Any], options: list[Any] | None = None) -> ModelType | None:
        statement = select(self._model).filter(*filters)
        if options:
            statement = statement.options(*options)

        return await self._session.scalar(statement=statement)

    async def update(self, _id: Any, obj: dict) -> ModelType:
        result = await self._session.execute(
            statement=update(self._model).filter(and_(self._model.id == _id)).values(**obj).returning(self._model)
        )
        await self._session.commit()
        return result.scalar_one_or_none()

    async def delete(self, _id: Any) -> ModelType:
        result = await self._session.execute(
            statement=delete(self._model).filter(and_(self._model.id == _id)).returning(self._model)
        )
        await self._session.commit()
        return result.scalar_one_or_none()

    async def get_list(
        self,
        page: int,
        page_size: int,
        options: list[Any] | None = None,
        filters: list[Any] | None = None,
    ) -> Sequence[Any | ModelType]:
        statement = select(self._model)
        if options:
            statement = statement.options(*options)
        if filters:
            statement = statement.filter(*filters)

        statement = statement.offset(page * page_size - page_size).limit(page_size)
        result = await self._session.scalars(statement=statement)
        return result.unique().all()

    async def count(
        self,
        filters: list[Any] | None = None,
    ) -> int:
        statement = select(func.count(self._model.id))
        if filters:
            statement = statement.filter(*filters)
        return await self._session.scalar(statement=statement)
