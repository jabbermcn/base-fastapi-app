from pydantic import MongoDsn, PostgresDsn

from settings._base import BaseSettingsWithConfig


__all__ = ["DatabaseSettings"]


class DatabaseSettings(BaseSettingsWithConfig, env_prefix="DATABASE_"):
    POSTGRES_DSN: PostgresDsn
    MONGO_DSN: MongoDsn
    MONGO_DATABASE_NAME: str
