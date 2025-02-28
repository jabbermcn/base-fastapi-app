from sqlalchemy.ext.asyncio import AsyncSession

from api.exeptions import IncorrectPasswordException, ObjectExistsException, ObjectNotFoundException
from src.exceptions import IncorrectPasswordError, ObjectAlreadyExistError, ObjectNotFoundError
from src.services import AuthService
from src.types import SignInRequestDTO, SignUpRequestDTO, TokenPairDTO


__all__ = ["RESTAuthService"]


class RESTAuthService:
    def __init__(self, session: AsyncSession):
        self._auth_service = AuthService(session=session)

    async def sign_in(self, data: SignInRequestDTO) -> TokenPairDTO:
        try:
            return await self._auth_service.sign_in(data=data)
        except ObjectNotFoundError:
            raise ObjectNotFoundException(name="user")
        except IncorrectPasswordError:
            raise IncorrectPasswordException()

    async def sign_up(self, data: SignUpRequestDTO) -> None:
        try:
            await self._auth_service.sign_up(data=data)
        except ObjectAlreadyExistError:
            raise ObjectExistsException(name="user")
