from aiohttp import web

from .handlers import misc


def setup_routes_v1(app: web.Application) -> None:
    app.add_routes([
        # Miscellaneous
        web.get(
            path="/health",
            handler=misc.healthcheck,
            allow_head=False,
        ),
    ])
