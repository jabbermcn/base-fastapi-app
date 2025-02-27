from typing import Annotated

from fastapi import Depends

from api.dependencies.database_session import DBSession
from api.services import RESTUserService


__all__ = ["UserServiceDepends"]


async def _get_user_service(session: DBSession) -> RESTUserService:
    return RESTUserService(session=session)


UserServiceDepends = Annotated[RESTUserService, Depends(dependency=_get_user_service)]
