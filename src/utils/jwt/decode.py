from jwt import decode

from settings import settings
from src.types import TokenPayload
from src.utils.jwt.exeptions import DecodeError


__all__ = ["JWTDecodeMixin"]


class JWTDecodeMixin:
    """
    JWTDecodeManagerMixin.

    A utility class for decoding JSON Web Tokens (JWT) into their payloads,
    with specific methods for decoding access and refresh tokens.

    :method decode: Decodes a JWT string and returns the payload.
    :method decode_access_token: Decodes an access token using predefined
                                 settings from the configuration.
    :method decode_refresh_token: Decodes a refresh token using predefined
                                  settings from the configuration.
    """

    @classmethod
    async def decode(cls, token: str, key: str, algorithms: list[str]) -> TokenPayload:
        """
        Decodes a JWT string into a payload.

        :param token: The JWT string to be decoded.
        :param key: The secret key used to validate the JWT.
        :param algorithms: A list of algorithms allowed for decoding the JWT.
        :return: An instance of `TokenPayload` containing the decoded payload.
        """

        try:
            return TokenPayload(**decode(jwt=token, key=key, algorithms=algorithms))
        except Exception:
            raise DecodeError()

    @classmethod
    async def decode_access_token(cls, token: str) -> TokenPayload:
        """
        Decodes an access token using predefined settings.

        Uses the access secret key and algorithm defined in the application's
        settings to decode the token.

        :param token: The JWT string representing the access token.
        :return: An instance of `TokenPayload` containing the decoded payload.
        """

        return await cls.decode(
            token=token,
            key=settings.JWT.ACCESS_SECRET_KEY.get_secret_value(),
            algorithms=[settings.JWT.ACCESS_ALGORITHM],
        )

    @classmethod
    async def decode_refresh_token(cls, token: str) -> TokenPayload:
        """
        Decodes a refresh token using predefined settings.

        Uses the refresh secret key and algorithm defined in the application's
        settings to decode the token.

        :param token: The JWT string representing the refresh token.
        :return: An instance of `TokenPayload` containing the decoded payload.
        """

        return await cls.decode(
            token=token,
            key=settings.JWT.REFRESH_SECRET_KEY.get_secret_value(),
            algorithms=[settings.JWT.REFRESH_ALGORITHM],
        )
