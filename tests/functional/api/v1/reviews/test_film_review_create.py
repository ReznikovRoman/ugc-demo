import pytest

from tests.functional.api.constants import VALID_FILM_ID

from ..base import AuthClientTest


class TestFilmReviewCreate(AuthClientTest):
    """Тестирование создания пользовательской рецензии на фильм."""

    endpoint = "/api/v1/users/me/reviews/films/{film_id}"
    method = "post"
    format_url = True
    use_data = True
    location = "json"

    async def test_ok(self):
        """При корректном теле запроса клиент получает информацию о созданной рецензии."""
        url = f"/api/v1/users/me/reviews/films/{VALID_FILM_ID}"
        data = {"title": "Title 1", "review": "Text"}

        got = await self.client.post(url, json=data)

        assert got["id"] is not None
        assert got["title"] == data["title"]

    async def test_wrong_body(self):
        """При неверном теле запроса клиент получит ошибку."""
        url = f"/api/v1/users/me/reviews/films/{VALID_FILM_ID}"
        data = {"title": "Title 1"}

        await self.client.post(url, json=data, expected_status_code=422)

    async def test_review_from_same_user(self):
        """Если пользователь пытается создать вторую рецензию на тот же фильм, то клиент получит ошибку."""
        url = f"/api/v1/users/me/reviews/films/{VALID_FILM_ID}"
        data = {"title": "Title 1", "review": "Text"}
        await self.client.post(url, json=data)

        got = await self.client.post(url, json=data, expected_status_code=409)

        assert got["error"]["code"] == "resource_conflict"

    async def test_review_from_another_user(self, another_auth_client):
        """Разные пользователи могут оставлять рецензию на один и тот же фильм."""
        url = f"/api/v1/users/me/reviews/films/{VALID_FILM_ID}"
        data = {"title": "Title 1", "review": "Text"}

        first = await self.client.post(url, json=data)
        another = await another_auth_client.post(url, json=data)

        assert first["id"] != another["id"]

    @pytest.fixture
    async def pre_auth_invalid_access_token(self):
        data = {"title": "Test title", "review": "Text"}
        return {"film_id": VALID_FILM_ID, "data": data}

    @pytest.fixture
    async def pre_auth_no_credentials(self):
        data = {"title": "Test title", "review": "Text"}
        return {"film_id": VALID_FILM_ID, "data": data}
