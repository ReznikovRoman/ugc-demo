from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Type

import pytest

from ugc.main import create_app

from .testlib import APIClient

if TYPE_CHECKING:
    from aiohttp.web import Application

    from ugc.containers import Container


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def app() -> Application:
    app = await create_app()
    yield app
    app.container.unwire()


@pytest.fixture
def aiohttp_client_cls() -> Type[APIClient]:
    return APIClient


@pytest.fixture
def container(app) -> Container:
    return app.container


@pytest.fixture
async def client(aiohttp_client, app) -> APIClient:
    yield await aiohttp_client(app)
