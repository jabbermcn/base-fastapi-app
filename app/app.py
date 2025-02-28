from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from admin.authentication import AdminAuthenticationBackend
from admin.google.handlers import router as google_router
from admin.views import FeedbackAdminView, UserAdminView
from api import api
from app.openapi import DESCRIPTION, TAGS_METADATA
from settings import settings
from src.config import async_redis_client
from src.database.connection import async_session_maker
from src.middlewares import CleanPathMiddleware
from src.utils.rate_limit import fastapi_limiter


__all__ = ["get_application"]


def include_routers(app: FastAPI) -> None:
    app.include_router(router=api)
    app.include_router(router=google_router)


def mount_applications(app: FastAPI) -> None:
    app.mount(path="/statics", app=StaticFiles(directory="statics"), name="statics")


def setup_openapi(app: FastAPI) -> None:
    app.openapi()
    app.openapi_schema["info"]["x-logo"] = {"url": app.url_path_for("statics", path="logo.svg")}


def setup_docs(app: FastAPI) -> None:
    @app.get(path="/docs", include_in_schema=False)
    async def swagger_ui_html() -> HTMLResponse:
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,  # noqa
            title=app.title,  # noqa
            swagger_favicon_url=app.url_path_for("statics", path="icon.svg"),
            swagger_ui_parameters={
                "showExtensions": False,
                "filter": True,
            },
        )

    @app.get(path="/redoc", include_in_schema=False)
    async def redoc_ui_html() -> HTMLResponse:
        return get_redoc_html(
            openapi_url=app.openapi_url,  # noqa
            title=app.title,  # noqa
            redoc_favicon_url=app.url_path_for("statics", path="icon.svg"),
            redoc_js_url="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js",
        )


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
    app.add_middleware(
        middleware_class=SessionMiddleware,  # noqa
        secret_key=settings.ADMIN.SECRET_KEY.get_secret_value(),
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator:  # noqa
    FastAPICache.init(RedisBackend(redis=async_redis_client), prefix="fastapi-cache")
    await fastapi_limiter.setup(redis_url=settings.REDIS.DSN)
    yield
    await fastapi_limiter.close()


def get_application() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        title="APP title",
        version="0.0.1",
        description=DESCRIPTION,
        default_response_class=ORJSONResponse,
        docs_url=None,
        redoc_url=None,
        openapi_tags=TAGS_METADATA,
        terms_of_service="https://example.com/terms/",
        contact={
            "name": "Mikhailouski Mikalai",
            "url": "https://www.linkedin.com/in/%D0%BD%D0%B8%D0%BA%D0%BE%D0%BB%D0%B0%D0%B9-%D0%BC%D0%B8%D1%85%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9-612744246/",
            "email": "jabbermnc@gmail.com",
        },
    )

    include_routers(app=app)
    mount_applications(app=app)
    setup_middlewares(app=app)
    setup_docs(app=app)
    setup_openapi(app=app)

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
