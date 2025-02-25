from fastapi import APIRouter

from .handlers import router


__all__ = ["users"]


users = APIRouter(tags=["User"], prefix="/users")
users.include_router(router=router)
