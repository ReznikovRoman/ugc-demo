import pytest

from tests.functional.api.constants import INVALID_FILM_ID, VALID_FILM_ID

from ..base import BaseClientTest


class TestFilmRatingRetrieve(BaseClientTest):
    """Тестирование получения информации о рейтинге фильма."""

    endpoint = "/api/v1/ratings/films/{film_id}"
    method = "get"
    format_url = True

    async def test_ok(self, film_ratings):
        """Если в БД есть информация о рейтинге фильма, то клиент получит средний рейтинг."""
        url = f"/api/v1/ratings/films/{VALID_FILM_ID}"

        got = await self.client.get(url)

        assert int(got["rating"]) == 6

    async def test_no_film_ratings(self):
        """Если у фильма нет пользовательских рейтингов, то клиент получит пустой ответ."""
        url = f"/api/v1/ratings/films/{INVALID_FILM_ID}"
        await self.client.get(url, expected_status_code=204)

    @pytest.fixture
    async def film_ratings(self, auth_client, another_auth_client):
        url = f"/api/v1/users/me/ratings/films/{VALID_FILM_ID}"
        data = {"rating": 7}
        another_data = {"rating": 5}
        await auth_client.post(url, json=data, expected_status_code=202)
        await another_auth_client.post(url, json=another_data, expected_status_code=202)
