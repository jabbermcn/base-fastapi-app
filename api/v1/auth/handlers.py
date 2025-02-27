from fastapi import APIRouter, Depends
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_429_TOO_MANY_REQUESTS,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from api.dependencies import AuthServiceDepends
from src.types import SignInRequestDTO, SignUpRequestDTO, TokenPairDTO
from src.types.exceptions import (
    HTTPExceptionErrorDTO,
    IncorrectPasswordErrorDTO,
    ObjectAlreadyExistErrorDTO,
    ObjectNotFoundErrorDTO,
    ToManyRequestsErrorDTO,
)
from src.utils.rate_limit import RateLimiter


router = APIRouter()


@router.post(
    path="/sign_up",
    response_model=None,
    status_code=HTTP_201_CREATED,
    dependencies=[Depends(dependency=RateLimiter(times=3, seconds=1))],
    summary="Sign Up",
    description="""
#### Limits: 3 Request / 1 second
""",
    responses={
        HTTP_409_CONFLICT: {"model": ObjectAlreadyExistErrorDTO(name="user")},
        HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
    },
    name="sign_up",
)
async def sign_up(data: SignUpRequestDTO, service: AuthServiceDepends) -> None:
    return await service.sign_up(data=data)


@router.post(
    path="/sign_in",
    response_model=TokenPairDTO,
    status_code=HTTP_201_CREATED,
    dependencies=[Depends(dependency=RateLimiter(times=3, seconds=1))],
    summary="Sign In",
    description="""
#### Limits: 3 Request / 1 second
""",
    responses={
        HTTP_400_BAD_REQUEST: {"model": IncorrectPasswordErrorDTO},
        HTTP_404_NOT_FOUND: {"model": ObjectNotFoundErrorDTO(name="user")},
        HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
    },
    name="sign_in",
)
async def sign_in(data: SignInRequestDTO, service: AuthServiceDepends) -> TokenPairDTO:
    return await service.sign_in(data=data)
