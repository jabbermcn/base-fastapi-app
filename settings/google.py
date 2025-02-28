from pydantic import HttpUrl, SecretStr

from settings._base import BaseSettingsWithConfig


__all__ = ["GoogleSettings"]


class GoogleSettings(BaseSettingsWithConfig, env_prefix="GOOGLE_"):
    REDIRECT_URI: HttpUrl
    CLIENT_ID: SecretStr
    CLIENT_SECRET: SecretStr
