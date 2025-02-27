from datetime import timedelta

from orjson import dumps, loads
from redis.asyncio import Redis

from settings import settings
from src.utils.jwt import IncorrectJWTBanPayloadError, JWTStorageUnavailableError


__all__ = ["JWTStorage"]


class JWTStorage:
    storage_backend: Redis = Redis.from_url(url=settings.REDIS.DSN.unicode_string())

    @classmethod
    def generate_key(cls, key: str, prefix: str) -> str:
        """
        Generates a standardized key for storage.

        :param key: The base key to use.
        :param prefix: The prefix to add to the key.
        :return: A formatted string for use as a storage key.
        """

        return f"jwt_ban:{prefix}:{key}"

    @classmethod
    async def set(cls, key: str, value: dict | str, exp: int | timedelta | None) -> None:
        """
        Adds a key to the storage with an expiration time.

        :param key: The key to add.
        :param value: The value to associate with the key.
        :param exp: The expiration time for the key (in seconds).
        :raises StorageError: If an error occurs during the operation.
        """
        try:
            await cls.storage_backend.set(name=key, value=dumps(value), ex=exp)
        except Exception:
            raise JWTStorageUnavailableError()

    @classmethod
    async def get(cls, key: str) -> dict | str | None:
        """
        Retrieves the value associated with a key from the storage.

        :param key: The key to retrieve the value for.
        :return: The value as a dictionary if found, or None if not found.
        :raises StorageError: If an error occurs during the operation.
        """
        try:
            payload = await cls.storage_backend.get(key)
        except Exception:
            raise JWTStorageUnavailableError()
        else:
            if payload:
                try:
                    return loads(payload)
                except Exception:
                    raise IncorrectJWTBanPayloadError()
            return None
