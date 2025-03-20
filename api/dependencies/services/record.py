from typing import Annotated

from fastapi import Depends

from api.services.record import RESTRecordService
from src.repos.mongo.record import RecordRepo
from src.services.record.record import RecordService


__all__ = ["RecordServiceDepends"]


async def _get_record_service() -> RESTRecordService:
    repo = RecordRepo()
    return RESTRecordService(record_service=RecordService(repo=repo))


RecordServiceDepends = Annotated[RESTRecordService, Depends(dependency=_get_record_service)]
