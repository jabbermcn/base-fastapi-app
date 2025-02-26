from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from src.database.models import User
from src.exceptions import ObjectAlreadyExistError, ObjectNotFoundError
from src.services import UserService
from src.types import UserCreateDTO, UserDTO


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
