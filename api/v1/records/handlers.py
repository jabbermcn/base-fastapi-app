from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_429_TOO_MANY_REQUESTS,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from api.annotated_types.record import RecordID
from api.dependencies import TokenPayloadDepends
from api.dependencies.services.record import RecordServiceDepends
from src.types.exceptions import (
    HTTPExceptionErrorDTO,
    ObjectAlreadyExistErrorDTO,
    ObjectNotFoundErrorDTO,
    ToManyRequestsErrorDTO,
)
from src.types.record import RecordCreateRequestDTO, RecordDTO, RecordExtendedDTO
from src.utils.rate_limit import RateLimiter


router = APIRouter()


@router.get(
    path="/{id}/",
    status_code=HTTP_200_OK,
    dependencies=[Depends(dependency=RateLimiter(times=3, seconds=1))],
    response_model=RecordExtendedDTO,
    summary="Get Record",
    responses={
        HTTP_404_NOT_FOUND: {"model": ObjectNotFoundErrorDTO(name="record")},
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
        HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
    },
    name="get_record",
)
@cache(expire=60, namespace="record")
async def get_record(pk: RecordID, service: RecordServiceDepends, payload: TokenPayloadDepends) -> RecordExtendedDTO:
    return await service.get_record(record_id=pk, user_id=payload.get("sub"))


@router.post(
    path="/",
    status_code=HTTP_201_CREATED,
    dependencies=[Depends(dependency=RateLimiter(times=3, seconds=1))],
    response_model=RecordDTO,
    summary="Create Record",
    responses={
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
        HTTP_409_CONFLICT: {"model": ObjectAlreadyExistErrorDTO(name="record")},
        HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
    },
    name="create_record",
)
async def create_record(
    data: RecordCreateRequestDTO, service: RecordServiceDepends, payload: TokenPayloadDepends
) -> RecordDTO:
    return await service.create_record(data=data, user_id=payload.get("sub"))


# @router.delete(
#     path="/{id}/",
#     status_code=HTTP_204_NO_CONTENT,
#     dependencies=[Depends(dependency=RateLimiter(times=3, seconds=1))],
#     summary="Delete Record",
#     responses={
#         HTTP_404_NOT_FOUND: {"model": ObjectNotFoundErrorDTO(name="record")},
#         HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
#         HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
#     },
#     name="delete_record",
# )
# async def delete_record(pk: RecordID, service: RecordServiceDepends, payload: TokenPayloadDepends) -> None:
#     await service.delete_record(record_id=pk)
#
#
# @router.patch(
#     path="/{id}/",
#     status_code=HTTP_202_ACCEPTED,
#     dependencies=[Depends(dependency=RateLimiter(times=3, seconds=1))],
#     response_model=RecordDTO,
#     summary="Update Record",
#     responses={
#         HTTP_404_NOT_FOUND: {"model": ObjectNotFoundErrorDTO(name="record")},
#         HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
#         HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
#     },
#     name="update_record",
# )
# async def update_record(
#     pk: RecordID, data: RecordUpdateRequestDTO, service: RecordServiceDepends, payload: TokenPayloadDepends
# ) -> RecordDTO:
#     return await service.update_record(record_id=pk, data=data)
#
#
# @router.get(
#     path="/",
#     status_code=HTTP_200_OK,
#     dependencies=[Depends(dependency=RateLimiter(times=3, seconds=1))],
#     response_model=Paginator[RecordExtendedDTO],
#     summary="Get Records",
#     responses={
#         HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
#         HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
#     },
#     name="get_records",
# )
# @cache(expire=60, namespace="record")
# async def get_records(
#     service: RecordServiceDepends,
#     payload: TokenPayloadDepends,
#     page: PageQuery = 1,
#     page_size: PageSizeQuery = 20,
# ) -> Paginator[RecordExtendedDTO]:
#     return await service.get_records(page=page, page_size=page_size, user_id=payload.get("sub"))
