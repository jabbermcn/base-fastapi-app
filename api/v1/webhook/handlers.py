from fastapi import APIRouter


router = APIRouter()


@router.post(
    path="/webhook",
)
async def webhook():
    return {"status": "ok"}
