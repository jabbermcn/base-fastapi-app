from fastapi import APIRouter

from .webhook import webhook


__all__ = ["v1"]


v1 = APIRouter(prefix="/v1")
v1.include_router(router=webhook)
