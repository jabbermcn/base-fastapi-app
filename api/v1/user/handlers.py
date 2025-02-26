from fastapi import APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from api.annotated_types.user import UserID
from api.dependecies import UserServiceDI
from src.types import UserCreateDTO, UserDTO
from src.types.exceptions import HTTPExceptionModel, UserAlreadyExistErrorDTO, UserNotFoundErrorDTO


router = APIRouter()


@router.get(
    path="/{id}/",
    status_code=HTTP_200_OK,
    response_model=UserDTO,
    summary="Get User",
    responses={
        HTTP_404_NOT_FOUND: {"model": UserNotFoundErrorDTO},
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionModel},
    },
    name="user_get",
)
async def user_get(pk: UserID, service: UserServiceDI) -> UserDTO:
    return await service.get_user(user_id=pk)


@router.post(
    path="/",
    status_code=HTTP_201_CREATED,
    response_model=UserDTO,
    summary="Create User",
    responses={
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionModel},
        HTTP_409_CONFLICT: {"model": UserAlreadyExistErrorDTO},
    },
    name="user_create",
)
async def user_create(data: UserCreateDTO, service: UserServiceDI) -> UserDTO:
    return await service.create_user(data=data)


@router.delete(
    path="/{id}/",
    status_code=HTTP_204_NO_CONTENT,
    summary="Delete User",
    responses={
        HTTP_404_NOT_FOUND: {"model": UserNotFoundErrorDTO},
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionModel},
    },
    name="user_delete",
)
async def user_delete(pk: UserID, service: UserServiceDI) -> None:
    await service.delete_user(user_id=pk)
