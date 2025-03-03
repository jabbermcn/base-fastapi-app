from app.metrics.setup import setup_metrics
from app.middlewares.setup import setup_middlewares
from app.openapi.setup import setup_docs, setup_openapi
from app.routers.setup import include_routers
from app.sentry.setup import setup_sentry

from .app import get_application


__all__ = [
    "get_application",
    "setup_docs",
    "setup_openapi",
    "include_routers",
    "setup_metrics",
    "setup_sentry",
    "setup_middlewares",
]
