from math import ceil
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from src.database.models import User
from src.exceptions import ObjectAlreadyExistError, ObjectNotFoundError
from src.services import UserService
from src.types import UserCreateDTO, UserDTO, UserUpdateDTO
from src.types.pagination import Pagination, Paginator


__all__ = ["RESTUserService"]


class RESTUserService:
    def __init__(self, session: AsyncSession):
        self._user_service = UserService(session=session)

    async def get_user(self, user_id: UUID) -> UserDTO:
        try:
            return UserDTO.model_validate(await self._user_service.get(user_id=user_id))
        except ObjectNotFoundError:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="user not found")

    async def create_user(self, data: UserCreateDTO) -> UserDTO:
        try:
            return UserDTO.model_validate(await self._user_service.create(user=User(**data.model_dump())))
        except ObjectAlreadyExistError:
            raise HTTPException(status_code=HTTP_409_CONFLICT, detail="user already exist")

    async def delete_user(self, user_id: UUID) -> None:
        try:
            await self._user_service.delete(user_id=user_id)
        except ObjectNotFoundError:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="user not found")

    async def update_user(self, user_id: UUID, data: UserUpdateDTO) -> UserDTO:
        try:
            return UserDTO.model_validate(
                await self._user_service.update(user_id=user_id, data=data.model_dump(exclude_unset=True))
            )
        except ObjectNotFoundError:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="user not found")

    async def get_users(self, page: int, page_size: int) -> Paginator[UserDTO]:
        return Paginator(
            results=[
                UserDTO.model_validate(user)
                for user in await self._user_service.get_list(page=page, page_size=page_size)
            ],
            pagination=Pagination(
                page_size=page_size,
                page=page,
                page_count=ceil(await self._user_service.count() / page_size),
            ),
        )
