import pytest

from tests.functional.api.constants import VALID_FILM_ID, VALID_USER_ID

from ..base import AuthClientTest


class TestFilmRatingCreate(AuthClientTest):
    """Тестирование добавления пользовательского рейтинга фильму."""

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

    async def test_same_user(self):
        """Один пользователь может оставить только один рейтинг к фильму или изменить его."""
        url = f"/api/v1/users/me/ratings/films/{VALID_FILM_ID}"
        data_first = {"rating": 10}
        rating_last = 5
        data_last = {"rating": rating_last}

        await self.client.post(url, json=data_first, expected_status_code=202)

        got = await self.client.post(url, json=data_last, expected_status_code=202)

        assert int(got["rating"]) == rating_last

    async def test_different_users(self, another_auth_client):
        """Разные пользователи могут добавить свой рейтинг к фильму."""
        url = f"/api/v1/users/me/ratings/films/{VALID_FILM_ID}"
        data = {"rating": 7}
        another_data = {"rating": 5}

        await self.client.post(url, json=data, expected_status_code=202)
        await another_auth_client.post(url, json=another_data, expected_status_code=202)

    async def test_wrong_body_rating_not_integer(self):
        """Если клиент передает `rating` не числом, то он получит ошибку."""
        url = f"/api/v1/users/me/ratings/films/{VALID_FILM_ID}"
        rating = "XXX"
        data = {"rating": rating}

        await self.client.post(url, json=data, expected_status_code=422)

    async def test_wrong_body_rating(self):
        """Если клиент передает `rating` не в диапазоне от 1 до 10, то он получит ошибку."""
        url = f"/api/v1/users/me/ratings/films/{VALID_FILM_ID}"
        rating = 11
        data = {"rating": rating}

        await self.client.post(url, json=data, expected_status_code=422)

    @pytest.fixture
    async def pre_auth_invalid_access_token(self):
        data = {"rating": 10}
        return {"film_id": VALID_FILM_ID, "user_id": VALID_USER_ID, "data": data}

    @pytest.fixture
    async def pre_auth_no_credentials(self):
        data = {"rating": 10}
        return {"film_id": VALID_FILM_ID, "user_id": VALID_USER_ID, "data": data}
