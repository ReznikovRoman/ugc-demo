from aiohttp_apispec import setup_aiohttp_apispec, validation_middleware

from aiohttp import web


def init_apispec(app: web.Application) -> None:
    setup_aiohttp_apispec(
        app=app,
        title="Netflix UGC",
        version="v1",
        url="/docs/swagger.json",
        swagger_path="/docs",
    )
    app.middlewares.append(validation_middleware)
