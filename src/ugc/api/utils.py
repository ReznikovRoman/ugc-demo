from http import HTTPStatus
from typing import Any

import orjson

from aiohttp import web
from aiohttp.typedefs import LooseHeaders

from ugc.helpers import sentinel


def orjson_response(
    data: Any = sentinel,
    *,
    status: int = HTTPStatus.OK,
    reason: str | None = None,
    headers: LooseHeaders | None = None,
    content_type: str = "application/json",
) -> web.Response:
    """Вспомогательная функция для создания `web.Response` с использованием библиотеки `orjson`."""
    body = None
    if data is not sentinel:
        body = orjson.dumps(data)
    return web.Response(
        text=None,
        body=body,
        status=status,
        reason=reason,
        headers=headers,
        content_type=content_type,
    )
