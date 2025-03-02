from pathlib import Path
from typing import Annotated

from pydantic import Field

from settings._base import BaseSettingsWithConfig
from settings.admin import AdminSettings
from settings.database import DatabaseSettings
from settings.google import GoogleSettings
from settings.jwt import JWTSettings
from settings.redis import RedisSettings
from settings.sentry import SentrySettings
from settings.server import ServerSettings


__all__ = ["settings"]


class Settings(BaseSettingsWithConfig):
    BASE_DIR: Path = Path(__file__).parent.parent

    ADMIN: Annotated[AdminSettings, Field(default_factory=AdminSettings)]
    SERVER: Annotated[ServerSettings, Field(default_factory=ServerSettings)]
    DATABASE: Annotated[DatabaseSettings, Field(default_factory=DatabaseSettings)]
    JWT: Annotated[JWTSettings, Field(default_factory=JWTSettings)]
    REDIS: Annotated[RedisSettings, Field(default_factory=RedisSettings)]
    GOOGLE: Annotated[GoogleSettings, Field(default_factory=GoogleSettings)]
    SENTRY: Annotated[SentrySettings, Field(default_factory=SentrySettings)]


settings = Settings()
