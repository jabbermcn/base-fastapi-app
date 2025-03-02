from pydantic import HttpUrl

from settings._base import BaseSettingsWithConfig


__all__ = ["SentrySettings"]


class SentrySettings(BaseSettingsWithConfig, env_prefix="SENTRY_"):
    DSN: HttpUrl
