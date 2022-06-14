from http import HTTPStatus

from aiohttp_apispec import docs

from aiohttp import web


@docs(summary="Добавить фильм в закладки.")
async def bookmark_film(request: web.Request) -> web.Response:
    """Добавление фильма с `film_id` в закладки авторизованному пользователю."""
    # TODO: https://github.com/ReznikovRoman/netflix-ugc/issues/4: сделать базовое АПИ
    return web.json_response(status=HTTPStatus.ACCEPTED)
