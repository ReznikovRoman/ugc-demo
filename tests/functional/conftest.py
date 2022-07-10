from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pytest

from .settings import get_settings
from .testlib import create_anon_client, create_auth_client, flush_mongo, flush_redis, run_redis_migrations, setup_mongo

if TYPE_CHECKING:
    from .settings import Test
    from .testlib import APIClient

settings_ = get_settings()


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def anon_client() -> APIClient:
    anon_client_ = create_anon_client()
    yield anon_client_
    await anon_client_.close()


@pytest.fixture(scope="session")
async def auth_client() -> APIClient:
    auth_client_ = create_auth_client()
    yield auth_client_
    await auth_client_.close()


@pytest.fixture(scope="session")
async def another_auth_client() -> APIClient:
    auth_client_ = create_auth_client(user_email="another@gmail.com")
    yield auth_client_
    await auth_client_.close()


@pytest.fixture
def settings() -> Test:
    return settings_


@pytest.fixture(autouse=True)
async def _autoflush_db() -> None:
    try:
        yield
    finally:
        await flush_redis()
        await run_redis_migrations()


@pytest.fixture(autouse=True)
async def _autoflush_mongo() -> None:
    try:
        yield
    finally:
        await flush_mongo()
        await setup_mongo()
