from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_429_TOO_MANY_REQUESTS,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from api.annotated_types import PageQuery, PageSizeQuery, ProjectID
from api.dependencies import ProjectServiceDepends, TokenPayloadDepends
from src.types import ProjectCreateRequestDTO, ProjectDTO, ProjectExtendedDTO, ProjectUpdateRequestDTO
from src.types.exceptions import (
    HTTPExceptionErrorDTO,
    ObjectAlreadyExistErrorDTO,
    ObjectNotFoundErrorDTO,
    ToManyRequestsErrorDTO,
)
from src.types.pagination import Paginator
from src.utils.rate_limit import RateLimiter


router = APIRouter()


@router.get(
    path="/{id}/",
    status_code=HTTP_200_OK,
    dependencies=[Depends(dependency=RateLimiter(times=3, seconds=1))],
    response_model=ProjectExtendedDTO,
    summary="Get Project",
    responses={
        HTTP_404_NOT_FOUND: {"model": ObjectNotFoundErrorDTO(name="project")},
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
        HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
    },
    name="get_project",
)
@cache(expire=60, namespace="project")
async def get_project(
    pk: ProjectID, service: ProjectServiceDepends, payload: TokenPayloadDepends
) -> ProjectExtendedDTO:
    return await service.get_project(project_id=pk, user_id=payload.get("sub"))


@router.post(
    path="/",
    status_code=HTTP_201_CREATED,
    dependencies=[Depends(dependency=RateLimiter(times=3, seconds=1))],
    response_model=ProjectDTO,
    summary="Create Project",
    responses={
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
        HTTP_409_CONFLICT: {"model": ObjectAlreadyExistErrorDTO(name="project")},
        HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
    },
    name="create_project",
)
async def create_project(
    data: ProjectCreateRequestDTO, service: ProjectServiceDepends, payload: TokenPayloadDepends
) -> ProjectDTO:
    return await service.create_project(data=data, user_id=payload.get("sub"))


@router.delete(
    path="/{id}/",
    status_code=HTTP_204_NO_CONTENT,
    dependencies=[Depends(dependency=RateLimiter(times=3, seconds=1))],
    summary="Delete Project",
    responses={
        HTTP_404_NOT_FOUND: {"model": ObjectNotFoundErrorDTO(name="user")},
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
        HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
    },
    name="delete_project",
)
async def delete_project(pk: ProjectID, service: ProjectServiceDepends, payload: TokenPayloadDepends) -> None:
    await service.delete_project(project_id=pk, user_id=payload.get("sub"))


@router.patch(
    path="/{id}/",
    status_code=HTTP_202_ACCEPTED,
    dependencies=[Depends(dependency=RateLimiter(times=3, seconds=1))],
    response_model=ProjectDTO,
    summary="Update Project",
    responses={
        HTTP_404_NOT_FOUND: {"model": ObjectNotFoundErrorDTO(name="user")},
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
        HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
    },
    name="update_project",
)
async def update_project(
    pk: ProjectID, data: ProjectUpdateRequestDTO, service: ProjectServiceDepends, payload: TokenPayloadDepends
) -> ProjectDTO:
    return await service.update_project(project_id=pk, data=data, user_id=payload.get("sub"))


@router.get(
    path="/",
    status_code=HTTP_200_OK,
    dependencies=[Depends(dependency=RateLimiter(times=3, seconds=1))],
    response_model=Paginator[ProjectExtendedDTO],
    summary="Get Projects",
    responses={
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
        HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
    },
    name="get_projects",
)
@cache(expire=60, namespace="project")
async def get_projects(
    service: ProjectServiceDepends,
    payload: TokenPayloadDepends,
    page: PageQuery = 1,
    page_size: PageSizeQuery = 20,
) -> Paginator[ProjectExtendedDTO]:
    return await service.get_projects(page=page, page_size=page_size, user_id=payload.get("sub"))
