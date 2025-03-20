from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqladmin import Admin
from starlette.staticfiles import StaticFiles

from admin.authentication import AdminAuthenticationBackend
from admin.views import FeedbackAdminView, ProjectAdminView, UserAdminView
from app import include_routers, setup_docs, setup_metrics, setup_middlewares, setup_openapi, setup_sentry
from app.openapi import DESCRIPTION, TAGS_METADATA
from settings import settings
from src.config import alchemy_db_connection, async_redis_client
from src.config.database import mongo_db_connection
from src.database.mongo.models import Record, User
from src.utils.rate_limit import fastapi_limiter


__all__ = ["get_application"]


def mount_applications(app: FastAPI) -> None:
    app.mount(path="/statics", app=StaticFiles(directory="statics"), name="statics")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:  # noqa
    FastAPICache.init(RedisBackend(redis=async_redis_client), prefix="fastapi-cache")
    await fastapi_limiter.setup(redis_url=settings.REDIS.DSN)
    await init_beanie(
        database=mongo_db_connection.database,
        document_models=[Record, User],
    )
    yield
    await fastapi_limiter.close()
    await mongo_db_connection.close()


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
    setup_sentry(app)
    setup_metrics(app)

    admin = Admin(
        app=app,
        session_maker=alchemy_db_connection.session_maker,
        favicon_url=app.url_path_for("statics", path="icon.svg"),
        logo_url=app.url_path_for("statics", path="logo.svg"),
        authentication_backend=AdminAuthenticationBackend(secret_key=settings.ADMIN.SECRET_KEY.get_secret_value()),
    )
    admin.add_model_view(view=UserAdminView)
    admin.add_model_view(view=FeedbackAdminView)
    admin.add_model_view(view=ProjectAdminView)
    return app
