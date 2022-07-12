from tests.functional.api.constants import INVALID_FILM_ID, VALID_FILM_ID

from ..base import BaseClientTest


class TestFilmRatingRetrieve(BaseClientTest):
    """Тестирование получения информации о рейтинге фильма."""

    endpoint = "/api/v1/ratings/films/{film_id}"
    method = "get"
    format_url = True

    async def test_ok(self):
        """Если в БД есть информация о рейтинге фильма, то клиент получит средний рейтинг."""
        url = f"/api/v1/ratings/films/{VALID_FILM_ID}"
        # TODO: создание рейтингов у фильма - фикстура
        await self.client.get(url, expected_status_code=204)

    async def test_no_film_ratings(self):
        """Если у фильма нет пользовательских рейтингов, то клиент получит пустой ответ."""
        url = f"/api/v1/ratings/films/{INVALID_FILM_ID}"
        await self.client.get(url, expected_status_code=204)
