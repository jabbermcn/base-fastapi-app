import sentry_sdk

from fastapi import FastAPI
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from settings import settings


def setup_sentry(app: FastAPI) -> None:  # noqa
    sentry_sdk.init(
        dsn=settings.SENTRY.DSN,
        integrations=[SqlalchemyIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
        _experiments={
            "continuous_profiling_auto_start": True,
        },
    )
