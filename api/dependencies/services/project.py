from typing import Annotated

from fastapi import Depends

from api.dependencies.database_session import DBSession
from api.services import RESTProjectService


__all__ = ["ProjectServiceDepends"]


async def _get_project_service(session: DBSession) -> RESTProjectService:
    return RESTProjectService(session=session)


ProjectServiceDepends = Annotated[RESTProjectService, Depends(dependency=_get_project_service)]
