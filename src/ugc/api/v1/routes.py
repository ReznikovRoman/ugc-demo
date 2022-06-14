from aiohttp import web

from .handlers import misc, ugc


def setup_routes_v1(app: web.Application) -> None:
    app.add_routes([
        # UGC
        web.post(
            path="/users/me/bookmarks/films/{film_id}",
            handler=ugc.bookmark_film,
        ),

        # Miscellaneous
        web.get(
            path="/health",
            handler=misc.healthcheck,
            allow_head=False,
        ),
    ])
