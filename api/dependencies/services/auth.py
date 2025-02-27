from typing import Annotated

from fastapi import Depends, Security
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer

from api.dependencies.database_session import DBSession
from api.exeptions import TokenNotProvidedException
from api.services import RESTAuthService


__all__ = ["HTTPAuthorizationCredentialsDepends", "AuthServiceDepends"]


async def _authenticate(
    creds: Annotated[HTTPAuthorizationCredentials, Security(dependency=HTTPBearer(auto_error=False))],
) -> HTTPAuthorizationCredentials:
    if creds is None:
        raise TokenNotProvidedException()
    return creds


HTTPAuthorizationCredentialsDepends = Annotated[HTTPAuthorizationCredentials, Security(dependency=_authenticate)]


async def _get_auth_service(session: DBSession) -> RESTAuthService:
    return RESTAuthService(session=session)


AuthServiceDepends = Annotated[RESTAuthService, Depends(dependency=_get_auth_service)]
