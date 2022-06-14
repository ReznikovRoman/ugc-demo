from aiohttp import web

from ugc.api.apispec import init_apispec
from ugc.api.v1.routes import setup_routes_v1
from ugc.core.config import get_settings
from ugc.middleware.errors import exception_middleware

from .containers import Container

settings = get_settings()


async def create_app() -> web.Application:
    container = Container()

    container.config.from_pydantic(settings)

    container.configure_logging()

    app = web.Application(middlewares=[exception_middleware])
    app.container = container

    api_v1 = web.Application()

    setup_routes_v1(api_v1)
    init_apispec(api_v1)

    app.add_subapp("/api/v1/", api_v1)
    return app
