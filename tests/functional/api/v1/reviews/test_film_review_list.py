import pytest

from tests.functional.api.constants import VALID_FILM_ID

from ..base import BaseClientTest


class TestFilmReviewList(BaseClientTest):
    """Тестирование получения списка рецензий на фильм."""

    endpoint = "/api/v1/reviews/films/{film_id}"
    method = "get"
    format_url = True

    REVIEW_TITLE: str = "List 1"
    ANOTHER_REVIEW_TITLE: str = "List -1"

    async def test_ok(self, reviews):
        """Если у фильма уже есть рецензии, то клиент получает список с пагинацией."""
        url = f"/api/v1/reviews/films/{VALID_FILM_ID}"

        got = await self.client.get(url)

        assert got["cursor"] is not None
        assert len(got["data"]) == 2

    async def test_limit(self, reviews):
        """Если клиент выставляет лимит на количество рецензий, то он получит соответствующие результаты."""
        url = f"/api/v1/reviews/films/{VALID_FILM_ID}?limit=1"

        got = await self.client.get(url)

        assert got["cursor"] is not None
        assert len(got["data"]) == 1
        assert got["data"][0]["title"] == self.ANOTHER_REVIEW_TITLE

    async def test_pagination(self, reviews):
        """Рецензии выдаются клиенту с `cursor-based` пагинацией."""
        url_first_page = f"/api/v1/reviews/films/{VALID_FILM_ID}?limit=1"

        first_page = await self.client.get(url_first_page)
        cursor = first_page["cursor"]

        assert cursor is not None
        assert len(first_page["data"]) == 1
        assert first_page["data"][0]["title"] == self.ANOTHER_REVIEW_TITLE

        url_next_page = f"/api/v1/reviews/films/{VALID_FILM_ID}?limit=1&cursor={cursor}"
        next_page = await self.client.get(url_next_page)

        assert len(next_page["data"]) == 1
        assert next_page["data"][0]["title"] == self.REVIEW_TITLE

    async def test_no_reviews(self):
        """Если на фильм еще не оставили ни одной рецензии, то клиент получит пустой список."""
        url = f"/api/v1/reviews/films/{VALID_FILM_ID}"

        got = await self.client.get(url)

        assert got["cursor"] is None
        assert len(got["data"]) == 0

    @pytest.fixture
    async def reviews(self, auth_client, another_auth_client):
        url = f"/api/v1/users/me/reviews/films/{VALID_FILM_ID}"
        data = {"title": self.REVIEW_TITLE, "review": "Text 1"}
        another_data = {"title": self.ANOTHER_REVIEW_TITLE, "review": "Text 2"}
        await auth_client.post(url, json=data, expected_status_code=201)
        await another_auth_client.post(url, json=another_data, expected_status_code=201)
