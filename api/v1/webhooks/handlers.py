from fastapi import APIRouter


router = APIRouter()


@router.post(
    path="/",
)
async def webhook():
    return {"status": "ok"}
