from pydantic import SecretStr

from settings._base import BaseSettingsWithConfig


__all__ = ["AdminSettings"]


class AdminSettings(BaseSettingsWithConfig, env_prefix="ADMIN_"):
    USERNAME: str
    PASSWORD: SecretStr
    SECRET_KEY: SecretStr
