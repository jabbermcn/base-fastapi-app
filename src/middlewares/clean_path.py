import re

from starlette.datastructures import URL
from starlette.responses import RedirectResponse
from starlette.status import HTTP_308_PERMANENT_REDIRECT
from starlette.types import ASGIApp, Receive, Scope, Send


__all__ = ["CleanPathMiddleware"]


class CleanPathMiddleware:
    REGEX_PATTERN = re.compile(pattern=r"//+")

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] in {"http", "websocket"}:
            url = URL(scope=scope)
            if self.REGEX_PATTERN.search(string=url.path):
                clean_url = url.replace(path=self.REGEX_PATTERN.sub(repl="/", string=url.path))

                response = RedirectResponse(url=clean_url, status_code=HTTP_308_PERMANENT_REDIRECT)
                await response(scope, receive, send)
            else:
                await self.app(scope, receive, send)
