from fastapi import FastAPI
from sqladmin import Admin
from starlette.staticfiles import StaticFiles
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from admin.authentication import AdminAuthenticationBackend
from admin.views import FeedbackAdminView, UserAdminView
from settings import settings
from src.database.connection import async_session_maker


def get_application() -> FastAPI:
    app = FastAPI()
    app.add_middleware(middleware_class=ProxyHeadersMiddleware, trusted_hosts=["*"])
    statics = StaticFiles(directory=settings.BASE_DIR / "statics")
    app.mount(path="/statics", app=statics, name="statics")
    admin = Admin(
        app=app,
        session_maker=async_session_maker,
        favicon_url=app.url_path_for("statics", path="icon.svg"),
        logo_url=app.url_path_for("statics", path="logo.svg"),
        authentication_backend=AdminAuthenticationBackend(secret_key=settings.ADMIN.SECRET_KEY.get_secret_value()),
    )
    admin.add_model_view(view=UserAdminView)
    admin.add_model_view(view=FeedbackAdminView)
    return app
