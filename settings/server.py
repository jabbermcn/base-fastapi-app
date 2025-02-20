from pydantic import PositiveInt

from settings._base import BaseSettingsWithConfig


__all__ = ["ServerSettings"]


class ServerSettings(BaseSettingsWithConfig, env_prefix="SERVER_"):
    HOST: str
    PORT: PositiveInt
