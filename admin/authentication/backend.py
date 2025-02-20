from datetime import timedelta

from jwt import InvalidTokenError, decode, encode
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import Response

from settings import settings
from src.utils.datetime import now


__all__ = ["AdminAuthenticationBackend"]


class AdminAuthenticationBackend(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        if username != settings.ADMIN.USERNAME or password != settings.ADMIN.PASSWORD.get_secret_value():
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
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Response | bool:
        token = request.session.get("token")

        if not token:
            return False

        try:
            decode(
                jwt=token,
                key=settings.ADMIN.SECRET_KEY.get_secret_value(),
                algorithms=["HS256"],
                audience="admin",
                subject="admin",
            )
        except InvalidTokenError:
            return False
        return True
