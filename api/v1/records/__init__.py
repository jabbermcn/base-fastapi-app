from fastapi import APIRouter

from .handlers import router


__all__ = ["records"]


records = APIRouter(tags=["Record"], prefix="/records")
records.include_router(router=router)
