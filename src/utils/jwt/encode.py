from jwt import encode

from settings import settings
from src.types import TokenPayload


__all__ = ["JWTEncodeMixin"]


class JWTEncodeMixin:
    """
    JWTEncodeManagerMixin.

    A utility class for encoding JSON Web Tokens (JWT) with specific payloads
    and configurations for access and refresh tokens.

    :method encode: Encodes a payload into a JWT string using the provided
                    secret key and algorithm.
    :method encode_access_token: Encodes an access token using predefined
                                 settings from the configuration.
    :method encode_refresh_token: Encodes a refresh token using predefined
                                  settings from the configuration.
    """

    @classmethod
    async def encode(cls, payload: TokenPayload, key: str, algorithm: str) -> str:
        """
        Encodes a payload into a JWT string.

        :param payload: The payload data to be included in the JWT.
        :param key: The secret key used to sign the JWT.
        :param algorithm: The algorithm used for signing the JWT.
        :return: A JWT string.
        """

        return encode(
            payload=payload,
            key=key,
            algorithm=algorithm,
        )

    @classmethod
    async def encode_access_token(cls, payload: TokenPayload) -> str:
        """
        Encodes an access token using predefined settings.

        Uses the access secret key and algorithm defined in the application's
        settings.

        :param payload: The payload data to be included in the access token.
        :return: A JWT string representing the access token.
        """

        return await cls.encode(
            payload=payload,
            key=settings.JWT.ACCESS_SECRET_KEY.get_secret_value(),
            algorithm=settings.JWT.ACCESS_ALGORITHM,
        )

    @classmethod
    async def encode_refresh_token(cls, payload: TokenPayload) -> str:
        """
        Encodes a refresh token using predefined settings.

        Uses the refresh secret key and algorithm defined in the application's
        settings.

        :param payload: The payload data to be included in the refresh token.
        :return: A JWT string representing the refresh token.
        """

        return await cls.encode(
            payload=payload,
            key=settings.JWT.REFRESH_SECRET_KEY.get_secret_value(),
            algorithm=settings.JWT.REFRESH_ALGORITHM,
        )
