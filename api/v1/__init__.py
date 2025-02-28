from fastapi import APIRouter

from .auth import auth
from .projects import projects
from .webhooks import webhooks


__all__ = ["v1"]


v1 = APIRouter(prefix="/v1")
v1.include_router(router=webhooks)
v1.include_router(router=projects)
v1.include_router(router=auth)
