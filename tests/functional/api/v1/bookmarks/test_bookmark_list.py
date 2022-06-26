from tests.functional.api.constants import VALID_FILM_ID

from ..base import AuthClientTest


class TestBookmarkList(AuthClientTest):
    """Тестирование получения списка закладок пользователя."""

    endpoint = "/api/v1/users/me/bookmarks/films"
    method = "get"

    async def test_ok(self):
        """Если у пользователя есть закладки, то клиент получит этот список."""
        await self.client.post(f"/api/v1/users/me/bookmarks/films/{VALID_FILM_ID}", expected_status_code=202)

        got = await self.client.get(self.endpoint)

        assert len(got) == 1
        assert got[0]["film_id"] == VALID_FILM_ID

    async def test_no_bookmarks(self):
        """Если у пользователя нет закладок фильмов, то клиент получит пустой список."""
        got = await self.client.get(self.endpoint)

        assert len(got) == 0
