from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from starlette.responses import HTMLResponse


__all__ = ["setup_docs", "setup_openapi"]


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


def setup_openapi(app: FastAPI) -> None:
    app.openapi()
    app.openapi_schema["info"]["x-logo"] = {"url": app.url_path_for("statics", path="logo.svg")}
