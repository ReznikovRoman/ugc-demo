import pytest

from tests.functional.api.constants import VALID_FILM_ID

from ..base import AuthClientTest


class TestBookmarkCreate(AuthClientTest):
    """Тестирование добавления закладки фильма."""

    endpoint = "/api/v1/users/me/bookmarks/films/{film_id}"
    method = "post"
    format_url = True

    async def test_ok(self):
        """При корректном запросе клиент получает сообщение об успешном сохранении в очередь."""
        url = f"/api/v1/users/me/bookmarks/films/{VALID_FILM_ID}"

        await self.client.post(url, expected_status_code=202)

    @pytest.fixture
    async def pre_auth_invalid_access_token(self):
        return {"film_id": VALID_FILM_ID}

    @pytest.fixture
    async def pre_auth_no_credentials(self):
        return {"film_id": VALID_FILM_ID}
