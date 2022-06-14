from typing import Awaitable, Callable

from aiohttp import web

from ugc.common.exceptions import NetflixUGCError


@web.middleware
async def exception_middleware(request: web.Request, handler: Callable[..., Awaitable]) -> web.Response:
    try:
        response = await handler(request)
    except NetflixUGCError as exc:
        return web.json_response(exc.to_dict(), status=exc.status_code)
    return response
