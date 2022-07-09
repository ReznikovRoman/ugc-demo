from aiohttp import web

from .handlers import misc, ugc


def setup_routes_v1(app: web.Application) -> None:
    app.add_routes([
        # Bookmarks
        web.post(
            path="/users/me/bookmarks/films/{film_id}",
            handler=ugc.add_film_bookmark,
        ),
        web.delete(
            path="/users/me/bookmarks/films/{film_id}",
            handler=ugc.delete_film_bookmark,
        ),
        web.get(
            path="/users/me/bookmarks/films",
            handler=ugc.get_user_films_bookmarks,
            allow_head=False,
        ),

        # Progress
        web.post(
            path="/users/me/progress/films/{film_id}",
            handler=ugc.track_film_progress,
        ),
        web.get(
            path="/users/me/progress/films/{film_id}",
            handler=ugc.get_film_progress,
            allow_head=False,
        ),

        # Reviews
        web.post(
            path="/users/me/reviews/films/{film_id}",
            handler=ugc.create_film_review,
        ),

        # Miscellaneous
        web.get(
            path="/health",
            handler=misc.healthcheck,
            allow_head=False,
        ),
    ])
