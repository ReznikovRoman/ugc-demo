from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union
from urllib.parse import urljoin

import aioredis
import orjson
from aredis_om import Migrator

import aiohttp
from aiohttp import ClientSession

from .settings import get_settings

if TYPE_CHECKING:
    from aiohttp import ClientResponse

    APIResponse = Union[dict, str, list[dict], dict[str, Any]]

settings = get_settings()


class APIClient(ClientSession):
    """Aiohttp клиент для функциональных тестов.

    Поддерживаются анонимный и авторизованный клиенты.
    """

    _access_token: str = None

    def __init__(
        self,
        base_url: str | None = settings.SERVER_BASE_URL,
        use_authorization: bool | None = False,
        *args, **kwargs,
    ):
        super().__init__(base_url, *args, **kwargs)
        self.base_url = base_url
        self.use_authorization = use_authorization
        self.auth_url = settings.NETFLIX_AUTH_BASE_URL

    async def _request(self, method, url, *args, **kwargs):
        headers = kwargs.pop("headers", {})
        anon = kwargs.pop("anon", False)
        if self.use_authorization and not anon:
            access_token = await self.get_access_token()
            headers.update({"Authorization": f"Bearer {access_token}"})
        response = await super(APIClient, self)._request(method, url, headers=headers, **kwargs)
        return response

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

    async def get_access_token(self) -> str:
        if self._access_token is not None:
            return self._access_token
        return await self._get_access_token()

    async def _get_access_token(self) -> str:
        body = {"email": "test@gmail.com", "password": "pass"}
        async with aiohttp.ClientSession() as session:
            async with session.post(urljoin(self.auth_url, "/api/v1/auth/register"), data=body):
                ...
            async with session.post(urljoin(self.auth_url, "/api/v1/auth/login"), data=body) as response:
                _response = await response.json()
                credentials = _response["data"]
                access_token = credentials["access_token"]
                self._access_token = access_token
                return access_token


def create_anon_client() -> APIClient:
    return APIClient(base_url=settings.CLIENT_BASE_URL)


def create_auth_client() -> APIClient:
    return APIClient(base_url=settings.CLIENT_BASE_URL, use_authorization=True)


async def run_redis_migrations() -> None:
    await Migrator("src.ugc").run()


async def flush_redis() -> None:
    redis_client = aioredis.from_url(settings.REDIS_OM_URL)
    await redis_client.flushdb()
