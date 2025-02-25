from fastapi import APIRouter
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from api.annotated_types.user import UserID
from api.dependecies import UserService
from src.types import UserDTO
from src.types.exceptions import HTTPExceptionModel, UserNotFoundErrorDTO


router = APIRouter()


@router.get(
    path="/{id}",
    status_code=HTTP_200_OK,
    response_model=UserDTO,
    summary="Get User",
    responses={
        HTTP_404_NOT_FOUND: {"model": UserNotFoundErrorDTO},
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionModel},
    },
    name="user_get",
)
async def user_get(pk: UserID, service: UserService) -> UserDTO:
    return await service.get_user(user_id=pk)
