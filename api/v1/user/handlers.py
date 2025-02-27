from fastapi import APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from api.annotated_types import PageQuery, PageSizeQuery, UserID
from api.dependencies import UserServiceDepends
from src.types import UserCreateDTO, UserDTO, UserUpdateDTO
from src.types.exceptions import HTTPExceptionErrorDTO, ObjectAlreadyExistErrorDTO, ObjectNotFoundErrorDTO
from src.types.pagination import Paginator


router = APIRouter()


@router.get(
    path="/{id}/",
    status_code=HTTP_200_OK,
    response_model=UserDTO,
    summary="Get User",
    responses={
        HTTP_404_NOT_FOUND: {"model": ObjectNotFoundErrorDTO(name="user")},
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
    },
    name="user_get",
)
async def user_get(pk: UserID, service: UserServiceDepends) -> UserDTO:
    return await service.get_user(user_id=pk)


@router.post(
    path="/",
    status_code=HTTP_201_CREATED,
    response_model=UserDTO,
    summary="Create User",
    responses={
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
        HTTP_409_CONFLICT: {"model": ObjectAlreadyExistErrorDTO(name="user")},
    },
    name="user_create",
)
async def user_create(data: UserCreateDTO, service: UserServiceDepends) -> UserDTO:
    return await service.create_user(data=data)


@router.delete(
    path="/{id}/",
    status_code=HTTP_204_NO_CONTENT,
    summary="Delete User",
    responses={
        HTTP_404_NOT_FOUND: {"model": ObjectNotFoundErrorDTO(name="user")},
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
    },
    name="user_delete",
)
async def user_delete(pk: UserID, service: UserServiceDepends) -> None:
    await service.delete_user(user_id=pk)


@router.patch(
    path="/{id}/",
    status_code=HTTP_202_ACCEPTED,
    response_model=UserDTO,
    summary="Update User",
    responses={
        HTTP_404_NOT_FOUND: {"model": ObjectNotFoundErrorDTO(name="user")},
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
    },
    name="user_update",
)
async def user_update(pk: UserID, data: UserUpdateDTO, service: UserServiceDepends) -> UserDTO:
    return await service.update_user(user_id=pk, data=data)


@router.get(
    path="/",
    status_code=HTTP_200_OK,
    response_model=Paginator[UserDTO],
    summary="Get Users",
    responses={
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
    },
    name="user_get_list",
)
async def user_get_list(
    service: UserServiceDepends,
    page: PageQuery = 1,
    page_size: PageSizeQuery = 20,
) -> Paginator[UserDTO]:
    return await service.get_users(page=page, page_size=page_size)
