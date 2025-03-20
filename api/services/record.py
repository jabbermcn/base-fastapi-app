from math import ceil
from uuid import UUID

from pydantic import ValidationError

from api.exception_handlers.factory import ExceptionHandlerFactory
from api.exeptions import (
    FastAPICacheException,
    InternalServerException,
    ObjectExistsException,
    ObjectNotFoundException,
    ServiceResponseValidationException,
)
from src.exceptions import FastAPICacheError, ObjectAlreadyExistError, ObjectNotFoundError
from src.services.record.record import RecordService
from src.types.pagination import Pagination, Paginator
from src.types.record import RecordCreateRequestDTO, RecordDTO, RecordExtendedDTO, RecordUpdateRequestDTO


record_exception_handler = ExceptionHandlerFactory(
    exc_mapping={
        ValidationError: ServiceResponseValidationException(name="record"),
        ObjectNotFoundError: ObjectNotFoundException(name="record"),
        ObjectAlreadyExistError: ObjectExistsException(name="record"),
        FastAPICacheError: FastAPICacheException(name="record"),
    },
    default_exc=InternalServerException(name="record"),
)


class RESTRecordService:
    def __init__(self, record_service: RecordService):
        self._record_service = record_service

    @record_exception_handler()
    async def get_record(self, record_id: UUID | str, user_id: UUID | str) -> RecordExtendedDTO:
        record = await self._record_service.get(
            record_id=record_id,
            user_id=user_id,
        )
        return RecordExtendedDTO.model_validate(record)

    @record_exception_handler()
    async def create_record(self, user_id: UUID | str, data: RecordCreateRequestDTO) -> RecordDTO:
        record = await self._record_service.create(
            user_id=user_id,
            data=data,
        )
        return RecordDTO.model_validate(record)

    @record_exception_handler()
    async def delete_record(self, record_id: UUID | str) -> None:
        await self._record_service.delete(record_id=record_id)

    @record_exception_handler()
    async def update_record(self, record_id: UUID | str, data: RecordUpdateRequestDTO) -> RecordDTO:
        record = await self._record_service.update(
            record_id=record_id,
            data=data,
        )
        return RecordDTO.model_validate(record)

    @record_exception_handler()
    async def get_records(self, user_id: UUID | str, page: int, page_size: int) -> Paginator[RecordExtendedDTO]:
        count = await self._record_service.count(user_id=user_id)
        records = await self._record_service.get_list(
            user_id=user_id,
            page=page,
            page_size=page_size,
        )

        return Paginator(
            results=[RecordExtendedDTO.model_validate(record) for record in records],
            pagination=Pagination(
                page_size=page_size,
                page=page,
                page_count=ceil(count / page_size) if count > 0 else 1,
            ),
        )
