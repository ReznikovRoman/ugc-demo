from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

from orjson import orjson

from aiohttp.test_utils import TestClient

if TYPE_CHECKING:
    from aiohttp import ClientResponse

    APIResponse = Union[dict, str, list[dict], dict[str, Any]]


class APIClient(TestClient):
    """API клиент для тестов."""

    def __init__(self, *args, **kwargs):
        super(APIClient, self).__init__(*args, **kwargs)

    async def _request(self, method: str, path: str, **kwargs: Any) -> ClientResponse:
        headers = kwargs.pop("headers", {})
        headers.update({"X-Request-Id": "XXX-XXX-XXX"})
        return await super(APIClient, self)._request(method, path, headers=headers, **kwargs)

    async def head(self, *args, **kwargs) -> APIResponse:
        return await self._api_call("head", kwargs.get("expected_status_code", 200), *args, **kwargs)

    async def get(self, *args, **kwargs) -> APIResponse:
        return await self._api_call("get", kwargs.get("expected_status_code", 200), *args, **kwargs)

    async def post(self, *args, **kwargs) -> APIResponse:
        return await self._api_call("post", kwargs.get("expected_status_code", 201), *args, **kwargs)

    async def put(self, *args, **kwargs) -> APIResponse:
        return await self._api_call("put", kwargs.get("expected_status_code", 200), *args, **kwargs)

    async def patch(self, *args, **kwargs) -> APIResponse:
        return await self._api_call("patch", kwargs.get("expected_status_code", 200), *args, **kwargs)

    async def delete(self, *args, **kwargs) -> APIResponse:
        return await self._api_call("delete", kwargs.get("expected_status_code", 204), *args, **kwargs)

    async def _api_call(self, method: str, expected: int, *args, **kwargs) -> APIResponse:
        kwargs.pop("expected_status_code", None)
        as_response = kwargs.pop("as_response", False)

        method = getattr(super(), method)
        response = await method(*args, **kwargs)

        if as_response:
            return response

        content = await self._decode(response)

        error_message = f"Got {response.status} instead of {expected}. Content is '{content}'"
        assert response.status == expected, error_message

        return content

    async def _decode(self, response: ClientResponse) -> APIResponse:
        content = await response.content.read()
        decoded = content.decode("utf-8", errors="ignore")
        if self.is_json(response) and content:
            return orjson.loads(decoded)
        return decoded

    @staticmethod
    def is_json(response: ClientResponse) -> bool:
        if response.headers:
            return "json" in response.headers.get("content-type")
        return False


def create_anon_client() -> APIClient:
    return APIClient()
