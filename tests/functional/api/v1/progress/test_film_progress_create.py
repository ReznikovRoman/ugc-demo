import pytest

from tests.functional.api.constants import VALID_FILM_ID

from ..base import AuthClientTest


class TestFilmProgressCreate(AuthClientTest):
    """Тестирование трекинга прогресса фильма."""

    endpoint = "/api/v1/users/me/progress/films/{film_id}"
    method = "post"
    format_url = True
    use_data = True
    location = "json"

    async def test_ok(self):
        """При корректном теле запроса клиент получает ответ об успешном сохранении сообщения в очередь."""
        url = f"/api/v1/users/me/progress/films/{VALID_FILM_ID}"
        frame = 1000
        data = {"viewed_frame": frame}

        await self.client.post(url, json=data, expected_status_code=202)

    async def test_wrong_body_frame_not_inger(self):
        """Если клиент передает `viewed_frame` не числом, то он получит ошибку."""
        url = f"/api/v1/users/me/progress/films/{VALID_FILM_ID}"
        frame = "XXX"
        data = {"viewed_frame": frame}

        await self.client.post(url, json=data, expected_status_code=422)

    async def test_wrong_body_negative_frame(self):
        """Если клиент передает `viewed_frame` как отрицательное число, то он получит ошибку."""
        url = f"/api/v1/users/me/progress/films/{VALID_FILM_ID}"
        frame = -123
        data = {"viewed_frame": frame}

        await self.client.post(url, json=data, expected_status_code=422)

    @pytest.fixture
    async def pre_auth_invalid_access_token(self):
        data = {"viewed_frame": 1000}
        return {"film_id": VALID_FILM_ID, "data": data}

    @pytest.fixture
    async def pre_auth_no_credentials(self):
        data = {"viewed_frame": 1000}
        return {"film_id": VALID_FILM_ID, "data": data}
