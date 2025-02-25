from collections.abc import Sequence
from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.exceptions import ObjectNotFoundError
from src.repos import UserRepo


__all__ = ["UserService"]


class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepo(session=session)

    async def get(self, user_id: UUID, options: list[Any] | None = None, filters: list[Any] | None = None) -> User:
        user = await self.repo.get(_id=user_id, options=options, filters=filters)
        if not user:
            raise ObjectNotFoundError(name="user")
        return user

    async def create(self, user: User) -> User:
        return await self.repo.create(obj=user)

    async def update(self, user_id: UUID, user: User) -> User:
        return await self.repo.update(_id=user_id, obj=user)

    async def delete(self, user_id: UUID) -> None:
        await self.repo.delete(_id=user_id)

    async def get_list(
        self, options: list[Any] | None = None, filters: list[Any] | None = None, page: int = 1, page_size: int = 25
    ) -> Sequence[User | Any]:
        return await self.repo.get_list(page=page, page_size=page_size, options=options, filters=filters)

    async def count(self, filters: list[Any] | None = None) -> int:
        return await self.repo.count(filters=filters)
