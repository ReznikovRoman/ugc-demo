from aiohttp_apispec import docs

from aiohttp import web


@docs(summary="Проверить состояние сервиса.")
async def healthcheck(_: web.Request) -> web.Response:
    """Проверка состояния сервиса."""
    return web.json_response({"status": "ok"})
