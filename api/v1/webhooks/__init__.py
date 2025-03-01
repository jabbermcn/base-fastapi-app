from fastapi import APIRouter

from .handlers import router


__all__ = ["webhooks"]


webhooks = APIRouter(tags=["Webhook"], prefix="/webhooks")
webhooks.include_router(router=router)
