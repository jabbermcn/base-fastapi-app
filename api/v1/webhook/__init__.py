from fastapi import APIRouter

from .handlers import router


__all__ = ["webhook"]


webhook = APIRouter(tags=["Webhook"])
webhook.include_router(router=router)
