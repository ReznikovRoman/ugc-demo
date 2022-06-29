from typing import Any

import pytest

from tests.functional.settings import get_settings
from tests.functional.testlib import APIClient

settings = get_settings()

pytestmark = [pytest.mark.asyncio]


class BaseClientTest:
    """Базовый класс для тестов."""

    client: APIClient
    anon_client: APIClient
    endpoint: str
    method: str
    format_url: bool = False
    use_data: bool = False

    @pytest.fixture(autouse=True)
    def _setup(self, anon_client):
        self.client: APIClient = anon_client
        self.anon_client: APIClient = anon_client
        self.endpoint = self.endpoint.removesuffix("/")
        self.method = self.method.lower()


class AuthTestMixin:
    """Миксин для тестов с авторизацией."""

    location: str = "data"
    jwt_invalid_access_token_status_code: int = 401

    async def test_invalid_access_token(self, pre_auth_invalid_access_token):
        """Если access токен в заголовке неверный, то клиент получит ошибку."""
        headers = {"Authorization": "Bearer XXX"}
        method = getattr(self.anon_client, self.method)
        endpoint = self._format_endpoint(pre_auth_invalid_access_token)
        data = {self.location: self._format_body(pre_auth_invalid_access_token)}
        await method(
            endpoint, headers=headers, **data, expected_status_code=self.jwt_invalid_access_token_status_code)

    async def test_no_credentials(self, pre_auth_no_credentials):
        """Если access токена нет в заголовках, то клиент получит соответствующую ошибку."""
        method = getattr(self.anon_client, self.method)
        endpoint = self._format_endpoint(pre_auth_no_credentials)
        data = {self.location: self._format_body(pre_auth_no_credentials)}
        await method(endpoint, **data, expected_status_code=401)

    def _format_endpoint(self, inputs: Any) -> str:
        if not self.format_url:
            return self.endpoint
        if not isinstance(inputs, dict):
            return NotImplemented
        endpoint = self.endpoint.format(**inputs)
        return endpoint

    def _format_body(self, body: Any) -> dict | None:
        if not self.use_data:
            return None
        if isinstance(body, dict):
            return body["data"]
        return None

    @pytest.fixture
    async def pre_auth_no_credentials(self, *args, **kwargs):
        ...

    @pytest.fixture
    async def pre_auth_invalid_access_token(self, *args, **kwargs):
        ...


class AuthClientTest(
    AuthTestMixin,
    BaseClientTest,
):
    """Базовый класс для тестов с JWT авторизацией."""

    client: APIClient

    @pytest.fixture(autouse=True)
    def _setup(self, auth_client, anon_client):
        self.client: APIClient = auth_client
        self.anon_client: APIClient = anon_client
        self.endpoint = self.endpoint.removesuffix("/")
        self.method = self.method.lower()
