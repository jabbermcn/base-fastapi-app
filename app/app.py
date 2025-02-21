from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.staticfiles import StaticFiles
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from admin.authentication import AdminAuthenticationBackend
from admin.views import FeedbackAdminView, UserAdminView
from api import api
from settings import settings
from src.database.connection import async_session_maker
from src.middlewares import CleanPathMiddleware


__all__ = ["get_application"]


def include_routers(app: FastAPI) -> None:
    app.include_router(router=api)


def mount_applications(app: FastAPI) -> None:
    app.mount(path="/statics", app=StaticFiles(directory="statics"), name="statics")


def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(middleware_class=ProxyHeadersMiddleware, trusted_hosts=["*"])  # noqa
    app.add_middleware(middleware_class=GZipMiddleware)  # noqa
    app.add_middleware(middleware_class=TrustedHostMiddleware, allowed_hosts=("*",))  # noqa
    app.add_middleware(
        middleware_class=CORSMiddleware,  # noqa
        allow_origins=("*",),
        allow_methods=("*",),
        allow_headers=("*",),
        allow_credentials=True,
    )
    app.add_middleware(middleware_class=CleanPathMiddleware)  # noqa


def get_application() -> FastAPI:
    app = FastAPI(
        title="Base fastapi app with admin panel",
        description="Base fastapi app with admin panel",
        default_response_class=ORJSONResponse,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        openapi_tags=[
            {
                "name": "Webhook",
                "description": "Set Webhook",
                "externalDocs": {
                    "description": "Webhook external docs",
                    "url": "https://fastapi.tiangolo.com/",
                },
            },
        ],
        terms_of_service="https://example.com/terms/",
        contact={
            "name": "Mikhailouski Mikalai",
            "url": "https://www.linkedin.com/in/%D0%BD%D0%B8%D0%BA%D0%BE%D0%BB%D0%B0%D0%B9-%D0%BC%D0%B8%D1%85%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9-612744246/",
            "email": "jabbermnc@gmail.com",
        },
        license_info={
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        },
    )
    include_routers(app=app)
    mount_applications(app=app)
    setup_middlewares(app=app)

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
