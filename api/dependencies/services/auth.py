from typing import Annotated

from fastapi import Depends, Security
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer

from api.dependencies.database_session import DBSession
from api.exeptions import InvalidTokenOrExpiredException, TokenNotProvidedException
from api.services import RESTAuthService
from src.types import TokenPayload
from src.utils.jwt import DecodeError
from src.utils.jwt.manager import JWTManager


__all__ = ["HTTPAuthorizationCredentialsDepends", "TokenPayloadDepends", "AuthServiceDepends"]


async def _authenticate(
    creds: Annotated[HTTPAuthorizationCredentials, Security(dependency=HTTPBearer(auto_error=False))],
) -> HTTPAuthorizationCredentials:
    if creds is None:
        raise TokenNotProvidedException()
    return creds


HTTPAuthorizationCredentialsDepends = Annotated[HTTPAuthorizationCredentials, Security(dependency=_authenticate)]


async def _get_token_payload(credentials: HTTPAuthorizationCredentialsDepends) -> TokenPayload:
    try:
        return await JWTManager.decode_access_token(token=credentials.credentials)
    except DecodeError:
        raise InvalidTokenOrExpiredException()


TokenPayloadDepends = Annotated[TokenPayload, Depends(dependency=_get_token_payload)]


async def _get_auth_service(session: DBSession) -> RESTAuthService:
    return RESTAuthService(session=session)


AuthServiceDepends = Annotated[RESTAuthService, Depends(dependency=_get_auth_service)]
