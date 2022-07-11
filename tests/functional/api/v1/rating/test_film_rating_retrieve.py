import pytest

from tests.functional.api.constants import VALID_FILM_ID

from ..base import AuthClientTest


class TestFilmRatingRetrieve(AuthClientTest):
    """Тестирование получения информации о рейтинге фильма."""

    endpoint = "/api/v1/ratings/films/{VALID_FILM_ID}"
    method = "get"
    format_url = True

    async def test_ok(self):
        """Если в БД есть информация о рейтинге фильма, то клиент получит ее."""
        await self.client.get(self.endpoint)

    async def test_not_found(self):
        """Если фильма нет в БД, то пользователь получит ошибку."""
        await self.client.get("/api/v1/ratings/films/XXX", expected_status_code=404)

    @pytest.fixture
    async def pre_auth_invalid_access_token(self):
        return {"film_id": VALID_FILM_ID}

    @pytest.fixture
    async def pre_auth_no_credentials(self):
        return {"film_id": VALID_FILM_ID}
