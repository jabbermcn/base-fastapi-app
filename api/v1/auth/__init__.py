from fastapi import APIRouter

from .handlers import router


__all__ = ["auth"]


auth = APIRouter(tags=["Auth"], prefix="/auth")
auth.include_router(router=router)
