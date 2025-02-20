from pathlib import Path
from typing import Annotated

from pydantic import Field

from settings._base import BaseSettingsWithConfig
from settings.admin import AdminSettings
from settings.database import DatabaseSettings
from settings.server import ServerSettings


__all__ = ["settings"]


class Settings(BaseSettingsWithConfig):
    BASE_DIR: Path = Path(__file__).parent.parent

    ADMIN: Annotated[AdminSettings, Field(default_factory=AdminSettings)]
    SERVER: Annotated[ServerSettings, Field(default_factory=ServerSettings)]
    DATABASE: Annotated[DatabaseSettings, Field(default_factory=DatabaseSettings)]


settings = Settings()
