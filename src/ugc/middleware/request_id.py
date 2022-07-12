from typing import Awaitable, Callable

from loguru import logger

from aiohttp import web

from ugc.common.constants import REQUEST_ID_HEADER
from ugc.common.exceptions import RequiredHeaderMissingError


@web.middleware
async def request_id_middleware(request: web.Request, handler: Callable[..., Awaitable]) -> web.Response:
    """Обработка обязательного заголовка `X-Request-Id`."""
    request_id = request.headers.get(REQUEST_ID_HEADER)
    if not request_id:
        raise RequiredHeaderMissingError(message="Required header `X-Request-Id` is missing")
    _add_extra_logging_field(request_id)
    response = await handler(request)
    return response


def _add_extra_logging_field(request_id: str) -> None:
    logger.configure(extra={"request_id": request_id})
