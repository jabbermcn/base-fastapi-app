from fastapi import FastAPI

from admin.google.handlers import router as google_router
from api import api


__all__ = ["include_routers"]


def include_routers(app: FastAPI) -> None:
    app.include_router(router=api)
    app.include_router(router=google_router)
