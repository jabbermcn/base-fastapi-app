from fastapi import APIRouter

from .handlers import router


__all__ = ["projects"]


projects = APIRouter(tags=["Project"], prefix="/projects")
projects.include_router(router=router)
