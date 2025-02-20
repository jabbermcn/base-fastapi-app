from uvicorn import run

from settings import settings


if __name__ == "__main__":
    run(
        app="app:get_application",
        host=settings.SERVER.HOST,
        port=settings.SERVER.PORT,
        http="httptools",
        loop="uvloop",
        interface="asgi3",
        factory=True,
        reload=True,
    )
