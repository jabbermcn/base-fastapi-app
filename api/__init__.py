from fastapi import APIRouter

from .v1 import v1


__all__ = ["api"]


api = APIRouter(prefix="/api")
api.include_router(router=v1)
