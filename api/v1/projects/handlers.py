from fastapi import APIRouter
from fastapi_cache.decorator import cache
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from api.annotated_types import PageQuery, PageSizeQuery, ProjectID
from api.dependencies import ProjectServiceDepends, TokenPayloadDepends
from src.types import ProjectCreateRequestDTO, ProjectDTO, ProjectExtendedDTO, ProjectUpdateRequestDTO
from src.types.exceptions import HTTPExceptionErrorDTO, ObjectAlreadyExistErrorDTO, ObjectNotFoundErrorDTO
from src.types.pagination import Paginator


router = APIRouter()


@router.get(
    path="/{id}/",
    status_code=HTTP_200_OK,
    response_model=ProjectExtendedDTO,
    summary="Get Project",
    responses={
        HTTP_404_NOT_FOUND: {"model": ObjectNotFoundErrorDTO(name="project")},
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
    },
    name="get_project",
)
async def get_project(pk: ProjectID, service: ProjectServiceDepends) -> ProjectExtendedDTO:
    return await service.get_project(project_id=pk)


@router.post(
    path="/",
    status_code=HTTP_201_CREATED,
    response_model=ProjectDTO,
    summary="Create Project",
    responses={
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
        HTTP_409_CONFLICT: {"model": ObjectAlreadyExistErrorDTO(name="project")},
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
    summary="Delete Project",
    responses={
        HTTP_404_NOT_FOUND: {"model": ObjectNotFoundErrorDTO(name="user")},
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
    },
    name="delete_project",
)
async def delete_project(pk: ProjectID, service: ProjectServiceDepends) -> None:
    await service.delete_project(project_id=pk)


@router.patch(
    path="/{id}/",
    status_code=HTTP_202_ACCEPTED,
    response_model=ProjectDTO,
    summary="Update Project",
    responses={
        HTTP_404_NOT_FOUND: {"model": ObjectNotFoundErrorDTO(name="user")},
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
    },
    name="update_project",
)
async def update_project(pk: ProjectID, data: ProjectUpdateRequestDTO, service: ProjectServiceDepends) -> ProjectDTO:
    return await service.update_project(project_id=pk, data=data)


@router.get(
    path="/",
    status_code=HTTP_200_OK,
    response_model=Paginator[ProjectExtendedDTO],
    summary="Get Projects",
    responses={
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
    },
    name="get_projects",
)
@cache(expire=60)
async def get_projects(
    service: ProjectServiceDepends,
    page: PageQuery = 1,
    page_size: PageSizeQuery = 20,
) -> Paginator[ProjectExtendedDTO]:
    return await service.get_projects(page=page, page_size=page_size)
