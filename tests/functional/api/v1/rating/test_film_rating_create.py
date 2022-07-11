import pytest

from tests.functional.api.constants import VALID_FILM_ID, VALID_USER_ID

from ..base import AuthClientTest


class TestFilmRatingCreate(AuthClientTest):
    """Тестирование трекинга прогресса фильма."""

    endpoint = "/api/v1/users/me/ratings/films/{film_id}"
    method = "post"
    format_url = True
    use_data = True
    location = "json"

    async def test_ok(self):
        """При корректном теле запроса клиент получает ответ об успешном сохранении рейтинга в очередь."""
        url = f"/api/v1/users/me/ratings/films/{VALID_FILM_ID}"
        rating = 10
        data = {"rating": rating}

        await self.client.post(url, json=data, expected_status_code=202)

    async def test_wrong_body_rating_not_inger(self):
        """Если клиент передает `rating` не числом, то он получит ошибку."""
        url = f"/api/v1/users/me/ratings/films/{VALID_FILM_ID}"
        rating = "XXX"
        data = {"rating": rating}

        await self.client.post(url, json=data, expected_status_code=422)

    async def test_wrong_body_rating(self):
        """Если клиент передает `rating` не в диапазоне 1-10, то он получит ошибку."""
        url = f"/api/v1/users/me/ratings/films/{VALID_FILM_ID}"
        rating = 11
        data = {"rating": rating}

        await self.client.post(url, json=data, expected_status_code=422)

    @pytest.fixture
    async def pre_auth_invalid_access_token(self):
        return {"film_id": VALID_FILM_ID, "user_id": VALID_USER_ID, "rating": 10}

    @pytest.fixture
    async def pre_auth_no_credentials(self):
        return {"film_id": VALID_FILM_ID, "user_id": VALID_USER_ID, "rating": 10}
