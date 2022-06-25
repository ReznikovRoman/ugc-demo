import pytest

pytestmark = [pytest.mark.asyncio]


async def test_ok(client):
    """Проверка состояния сервиса работает корректно."""
    got = await client.get("/api/v1/health")

    assert got["status"] == "ok"
