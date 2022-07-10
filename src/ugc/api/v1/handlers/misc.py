from http import HTTPStatus

from aiohttp_apispec import docs

from aiohttp import web

from ugc.api.utils import orjson_response


@docs(tags=["misc"], summary="Проверить состояние сервиса.")
async def healthcheck(_: web.Request) -> web.Response:
    """Проверка состояния сервиса."""
    response = {"status": "ok"}
    return orjson_response(response, status=HTTPStatus.OK)
