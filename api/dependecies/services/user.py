from typing import Annotated

from fastapi import Depends

from api.dependecies.database_session import DBSession
from api.services import RESTUserService


__all__ = ["UserService"]


async def _get_user_service(session: DBSession) -> RESTUserService:
    return RESTUserService(session=session)


UserService = Annotated[RESTUserService, Depends(dependency=_get_user_service)]
