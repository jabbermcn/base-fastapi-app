from pydantic import PostgresDsn

from settings._base import BaseSettingsWithConfig


__all__ = ["DatabaseSettings"]


class DatabaseSettings(BaseSettingsWithConfig, env_prefix="DATABASE_"):
    DSN: PostgresDsn
