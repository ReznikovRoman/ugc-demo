import pytest

from tests.functional.api.constants import ANOTHER_FILM_ID, VALID_FILM_ID

from ..base import AuthClientTest


class TestBookmarkDelete(AuthClientTest):
    """Тестирование удаления закладки фильма."""

    endpoint = "/api/v1/users/me/bookmarks/films/{film_id}"
    method = "delete"
    format_url = True

    async def test_ok(self):
        """При корректном запросе клиент получает сообщение об успешном сохранении в очередь."""
        url = f"/api/v1/users/me/bookmarks/films/{VALID_FILM_ID}"

        await self.client.delete(url, expected_status_code=202)

    async def test_ignore_invalid_id(self):
        """Неверный ID фильма никак не проверяется на уровне АПИ, сообщение в любом случае отправляется в очередь.

        Например, если клиент попытается удалить несуществующую закладку фильма - он не получит сразу ошибку.
        """
        url = f"/api/v1/users/me/bookmarks/films/{VALID_FILM_ID}"
        await self.client.delete(url, expected_status_code=202)

        another_url = f"/api/v1/users/me/bookmarks/films/{ANOTHER_FILM_ID}"
        await self.client.delete(another_url, expected_status_code=202)

    @pytest.fixture
    async def pre_auth_invalid_access_token(self):
        return {"film_id": VALID_FILM_ID}

    @pytest.fixture
    async def pre_auth_no_credentials(self):
        return {"film_id": VALID_FILM_ID}
