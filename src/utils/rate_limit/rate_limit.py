from collections.abc import Callable
from math import ceil
from typing import NoReturn

from fastapi import HTTPException
from pydantic import RedisDsn
from redis.asyncio import Redis
from redis.commands.core import AsyncScript
from starlette.requests import Request
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
from starlette.websockets import WebSocket


async def default_identifier(request: Request | WebSocket):
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        ip = forwarded.split(",")[0]
    else:
        ip = request.client.host
    return ip + ":" + request.scope["path"]


async def http_default_callback(
    request: Request,
    expire: int,
) -> NoReturn:
    expire = ceil(expire / 1000)
    raise HTTPException(
        status_code=HTTP_429_TOO_MANY_REQUESTS,
        detail="to_many_requests",
        headers={"Retry-After": f"{expire}"},
    )


async def ws_default_callback(ws: WebSocket, expire: int) -> NoReturn:
    expire = ceil(expire / 1000)
    raise HTTPException(
        status_code=HTTP_429_TOO_MANY_REQUESTS,
        detail="to_many_requests",
        headers={"Retry-After": f"{expire}"},
    )


class FastAPILimiter:
    def __init__(self):
        self.redis: Redis | None = None
        self.prefix: str = "RATE_LIMIT"
        self.identifier: Callable = default_identifier
        self.http_callback: Callable[[Request, int], None] = http_default_callback
        self.ws_callback: Callable[[WebSocket, int], None] = ws_default_callback
        self.lua_script: AsyncScript | None = None
        self.raw_lua_script = self._load_lua_script()

    @staticmethod
    def _load_lua_script():
        with open(file="src/utils/rate_limit/rate_limit.lua") as f:
            return f.read()

    async def setup(
        self,
        redis_url: str | RedisDsn,
        identifier: Callable[[Request], str] = None,
        http_callback: Callable[[Request, int], None] = None,
        ws_callback: Callable[[WebSocket, int], None] = None,
    ) -> None:
        if isinstance(redis_url, RedisDsn):
            redis_url = redis_url.unicode_string()

        self.redis = Redis.from_url(url=redis_url)
        self.identifier = identifier or self.identifier
        self.http_callback = http_callback or self.http_callback
        self.ws_callback = ws_callback or self.ws_callback
        self.lua_script = self.redis.register_script(script=self.raw_lua_script)

    async def close(self) -> None:
        await self.redis.close()


fastapi_limiter = FastAPILimiter()


class RateLimiter:
    def __init__(
        self,
        times: int = 1,
        milliseconds: int = 0,
        seconds: int = 0,
        minutes: int = 0,
        hours: int = 0,
        identifier: Callable = None,
        callback: Callable = None,
    ):
        self.times = times
        self.milliseconds = milliseconds + 1000 * seconds + 60000 * minutes + 3600000 * hours
        self.identifier = identifier
        self.callback = callback

    async def _check(self, key: str) -> int:
        return await fastapi_limiter.lua_script(keys=[key], args=[f"{self.times}", f"{self.milliseconds}"])

    async def __call__(self, request: Request):
        if not fastapi_limiter.redis:
            raise Exception("You must call fastapi_limiter.setup in startup event of fastapi!")
        route_index = 0
        dep_index = 0
        for i, route in enumerate(request.app.routes):
            if route.path == request.scope["path"] and request.method in route.methods:
                route_index = i
                for j, dependency in enumerate(route.dependencies):
                    if self is dependency.dependency:
                        dep_index = j
                        break

        identifier = self.identifier or fastapi_limiter.identifier
        callback = self.callback or fastapi_limiter.http_callback
        rate_key = await identifier(request)
        key = f"{fastapi_limiter.prefix}:{rate_key}:{route_index}:{dep_index}"
        expire = await self._check(key)
        if expire != 0:
            await callback(request, expire)


class WebSocketRateLimiter(RateLimiter):
    async def __call__(self, ws: WebSocket, context_key=""):
        if not fastapi_limiter.redis:
            raise Exception("You must call fastapi_limiter.setup in startup event of fastapi!")
        identifier = self.identifier or fastapi_limiter.identifier
        rate_key = await identifier(ws)
        key = f"{fastapi_limiter.prefix}:ws:{rate_key}:{context_key}"
        expire = await self._check(key)
        callback = self.callback or fastapi_limiter.ws_callback
        if expire != 0:
            await callback(ws, expire)
