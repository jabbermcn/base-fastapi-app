"""This package contains base settings class."""

from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = ["BaseSettingsWithConfig"]


class BaseSettingsWithConfig(BaseSettings):
    """Base class for all settings.

    E.g.::

        from typing import Annotated

        from pydantic import Field
        from uvicorn import run
        from fastapi import FastAPI

        from settings._base import BaseSettingsWithConfig

        class ServerSettings(BaseSettingsWithConfig, env_prefix="SERVER_"):
            HOST: str
            PORT: int

        class Settings(BaseSettingsWithConfig):
            SERVER: Annotated[ServerSettings, Field(default_factory=ServerSettings)]

        settings = Settings()

        app = FastAPI()

        if __name__ == "__main__":
            run(app, host=settings.SERVER.HOST, port=settings.SERVER.PORT)
    """

    model_config = SettingsConfigDict(
        case_sensitive=False,
        str_strip_whitespace=True,
        use_enum_values=True,
        frozen=True,
        coerce_numbers_to_str=True,
    )
