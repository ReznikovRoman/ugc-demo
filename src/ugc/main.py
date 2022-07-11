import logging

from aiohttp import web

from ugc.api.apispec import init_apispec
from ugc.api.v1.routes import setup_routes_v1
from ugc.core.config import get_settings
from ugc.middleware.errors import exceptions_middleware
from ugc.middleware.request_id import request_id_middleware

from .containers import Container, get_processors, override_providers

settings = get_settings()


async def create_app() -> web.Application:
    container = Container()

    container.config.from_pydantic(settings)

    app = web.Application(middlewares=[request_id_middleware, exceptions_middleware])
    app.container = container

    api_v1 = web.Application()

    setup_routes_v1(api_v1)
    init_apispec(api_v1)

    override_providers(container)
    await container.init_resources()
    container.check_dependencies()

    processors = await get_processors(container)

    @app.on_startup.append
    async def _on_startup(_: web.Application) -> None:
        logging.info("Start server")
        for processor in processors:
            processor.start_processing()

    @app.on_cleanup.append
    async def _on_cleanup(_: web.Application) -> None:
        logging.info("Cleanup resources")
        for processor in processors:
            processor.stop_processing()
        await container.shutdown_resources()

    app.add_subapp("/api/v1/", api_v1)
    return app
