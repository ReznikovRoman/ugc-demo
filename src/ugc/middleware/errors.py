from typing import Awaitable, Callable

from aiohttp import web

from ugc.api.utils import orjson_response
from ugc.common.exceptions import NetflixUGCError


@web.middleware
async def exceptions_middleware(request: web.Request, handler: Callable[..., Awaitable]) -> web.Response:
    """Обработка ошибок проекта."""
    try:
        response = await handler(request)
    except NetflixUGCError as exc:
        return orjson_response(exc.to_dict(), status=exc.status_code)
    return response
