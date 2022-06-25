import pytest

pytestmark = [pytest.mark.asyncio]


async def test_ok(anon_client):
    """Проверка состояния сервиса работает корректно."""
    got = await anon_client.get("/api/v1/health")

    assert got["status"] == "ok"
