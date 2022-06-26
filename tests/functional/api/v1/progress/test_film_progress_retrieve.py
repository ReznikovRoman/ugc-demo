import pytest

from tests.functional.api.constants import VALID_FILM_ID

from ..base import AuthClientTest


class TestFilmProgressRetrieve(AuthClientTest):
    """Тестирование получения информации о прогрессе фильма."""

    endpoint = "/api/v1/users/me/progress/films/{film_id}"
    method = "get"
    format_url = True

    async def test_ok(self):
        """Если в БД есть информация о прогрессе фильма, то клиент получит ее."""
        url = f"/api/v1/users/me/progress/films/{VALID_FILM_ID}"
        frame = 1000
        data = {"viewed_frame": frame}
        await self.client.post(url, data=data, expected_status_code=202)

        got = await self.client.get(url)

        assert got["viewed_frame"] == frame

    async def test_latest_progress(self):
        """Если прогресс фильма обновлялся несколько раз, то клиент получит данные с последнего обновления."""
        url = f"/api/v1/users/me/progress/films/{VALID_FILM_ID}"
        data_first = {"viewed_frame": 500}
        frame_last = 1000
        data_last = {"viewed_frame": frame_last}
        await self.client.post(url, data=data_first, expected_status_code=202)
        await self.client.post(url, data=data_last, expected_status_code=202)

        got = await self.client.get(url)

        assert got["viewed_frame"] == frame_last

    async def test_not_found(self):
        """Если прогресса по данному фильму нет, то пользователь получит ошибку."""
        await self.client.get("/api/v1/users/me/progress/films/XXX", expected_status_code=404)

    @pytest.fixture
    async def pre_auth_invalid_access_token(self):
        return {"film_id": VALID_FILM_ID}

    @pytest.fixture
    async def pre_auth_no_credentials(self):
        return {"film_id": VALID_FILM_ID}
