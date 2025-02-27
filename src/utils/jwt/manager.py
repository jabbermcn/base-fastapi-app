from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from settings import settings
from src.enums import JWTPrefix
from src.exceptions.auth import TokenIsBannedError
from src.types import TokenPayload
from src.utils.datetime import now
from src.utils.jwt import JWTDecodeMixin, JWTEncodeMixin, JWTStorage


__all__ = ["JWTManager"]


class JWTManager(JWTEncodeMixin, JWTDecodeMixin):
    """
    Manages JSON Web Tokens (JWTs) for authentication.

    This class provides methods for creating, managing, and validating JWTs.
    It handles both access and refresh tokens, as well as token banning.
    """

    storage: JWTStorage = JWTStorage
    jti_generator: Callable[[], str] = lambda: f"{uuid4()}"
    JWT_ACCESS_EXP_TIME: timedelta = timedelta(minutes=settings.JWT.ACCESS_EXP_TIME)
    JWT_REFRESH_EXP_TIME: timedelta = timedelta(minutes=settings.JWT.REFRESH_EXP_TIME)

    @classmethod
    async def create_access_token(
        cls,
        user_id: str,
        jti: str,
    ) -> str:
        """
        Generate an access token for a user.

        :param user_id: The unique identifier of the user.
        :param jti: The JSON Token Identifier.
        :return: A string representing the encoded access token.
        """

        payload = TokenPayload(
            sub=f"{user_id}",
            iat=now(),
            exp=now() + cls.JWT_ACCESS_EXP_TIME,
            jti=jti,
        )
        return await cls.encode_access_token(payload)

    @classmethod
    async def create_refresh_token(
        cls,
        user_id: str,
        jti: str,
    ) -> str:
        """
        Generate a refresh token for a user.

        :param user_id: The unique identifier of the user.
        :param jti: The JSON Token Identifier.
        :return: A string representing the encoded refresh token.
        """

        payload = TokenPayload(
            sub=user_id,
            iat=now(),
            exp=now() + cls.JWT_REFRESH_EXP_TIME,
            jti=f"{jti}",
        )
        return await cls.encode_refresh_token(payload)

    @classmethod
    async def create_token_pair(cls, user_id: str | UUID) -> dict[str, str]:
        """
        Generate a pair of tokens (access and refresh).

        :param user_id: The unique identifier of the user (str or UUID).
        :return: A dictionary containing both access and refresh tokens.
        """

        if isinstance(user_id, UUID):
            user_id = f"{user_id}"

        jti = cls.jti_generator()

        return {
            "access_token": await cls.create_access_token(user_id=user_id, jti=jti),
            "refresh_token": await cls.create_refresh_token(user_id=user_id, jti=jti),
        }

    @classmethod
    async def ban_token_pair(
        cls,
        payload: TokenPayload,
        **kwargs,
    ) -> None:
        """
        Ban a token pair by storing its JTI (JSON Token Identifier).

        :param payload: The TokenPayload object containing token information.
        :param kwargs: Additional data to store alongside the banned token.
        :return: None
        """

        iat = payload.get("iat")
        if isinstance(iat, int | float):
            iat = datetime.fromtimestamp(iat, tz=UTC)

        await cls.storage.set(
            key=cls.storage.generate_key(key=payload.get("jti"), prefix=JWTPrefix.JTI),
            value={**kwargs, "jwt_jti": payload.get("jti")},
            exp=iat + timedelta(minutes=settings.JWT.REFRESH_EXP_TIME) - now(),
        )

    @classmethod
    async def ban_all_user_tokens(
        cls,
        user_id: str,
    ) -> None:
        """
        Ban all tokens associated with a user.

        :param user_id: The unique identifier of the user.
        :return: None
        """

        await cls.storage.set(
            key=cls.storage.generate_key(key=user_id, prefix=JWTPrefix.SUB),
            value=now().isoformat(),
            exp=timedelta(minutes=settings.JWT.REFRESH_EXP_TIME),
        )

    @classmethod
    async def is_token_banned(cls, payload: TokenPayload) -> bool:
        """
        Check if a token is banned or expired.

        :param payload: The TokenPayload object containing token information.
        :return: True if the token is banned or expired, False otherwise.
        """

        last_logout = await cls.storage.get(cls.storage.generate_key(key=payload.get("sub"), prefix=JWTPrefix.SUB))
        if last_logout:
            return datetime.fromtimestamp(payload.get("iat"), tz=UTC) <= datetime.fromisoformat(last_logout)
        if await JWTStorage.get(key=JWTStorage.generate_key(key=payload.get("jti"), prefix=JWTPrefix.JTI)):
            raise TokenIsBannedError()
        return False
