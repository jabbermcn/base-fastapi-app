from datetime import timedelta

from fastapi import APIRouter
from httpx import AsyncClient
from jwt import encode
from starlette.requests import Request
from starlette.responses import RedirectResponse

from settings import settings
from src.utils.datetime import now


router = APIRouter()


@router.get(path="/admin/google/login", name="google_login", include_in_schema=False)
async def google_login(request: Request):  # noqa
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings.GOOGLE.CLIENT_ID.get_secret_value()}"
        f"&redirect_uri={settings.GOOGLE.REDIRECT_URI.unicode_string()}&scope=openid%20profile%20email&access_type=offline"
    )

    return RedirectResponse(url=google_auth_url)


@router.get(path="/admin/google/callback", name="google_callback", include_in_schema=False)
async def google_callback(request: Request):
    async with AsyncClient() as client:
        url = "https://accounts.google.com/o/oauth2/token"
        data = {
            "code": request.query_params.get("code"),
            "client_id": settings.GOOGLE.CLIENT_ID.get_secret_value(),
            "client_secret": settings.GOOGLE.CLIENT_SECRET.get_secret_value(),
            "redirect_uri": settings.GOOGLE.REDIRECT_URI.unicode_string(),
            "grant_type": "authorization_code",
        }
        response = await client.post(url=url, data=data)
        user_info = await client.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {response.json().get('access_token')}"},
        )
        if user_info.json().get("email") not in settings.ADMIN.ALLOWED_EMAILS:
            return False

        request.session.update(
            {
                "token": encode(
                    payload={"exp": now() + timedelta(days=1), "sub": "admin", "aud": "admin"},
                    algorithm="HS256",
                    key=settings.ADMIN.SECRET_KEY.get_secret_value(),
                )
            }
        )

    return RedirectResponse(url="/admin")
