from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.exceptions import IncorrectPasswordError, ObjectAlreadyExistError, ObjectNotFoundError
from src.repos import UserRepo
from src.types import SignInRequestDTO, SignUpRequestDTO, TokenPairDTO
from src.utils.jwt.manager import JWTManager
from src.utils.password import PasswordManager


__all__ = ["AuthService"]


class AuthService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepo(session=session)

    async def sign_in(self, data: SignInRequestDTO) -> TokenPairDTO:
        user = await self.repo.get(filters=[User.email == data.email.lower()])
        if not user:
            raise ObjectNotFoundError(name="user")
        if not PasswordManager.check(plain_password=data.password, password_hash=user.password_hash):
            raise IncorrectPasswordError()
        return TokenPairDTO.model_validate(obj=await JWTManager.create_token_pair(user_id=user.id))

    async def sign_up(self, data: SignUpRequestDTO) -> User:
        user_data = data.model_dump(exclude={"password"})
        user_data["email"] = data.email.lower()
        user_data["password_hash"] = PasswordManager.hash(plain_password=data.password)
        try:
            return await self.repo.create(obj=user_data)
        except IntegrityError:
            raise ObjectAlreadyExistError(name="user")
