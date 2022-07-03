from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator

import motor.motor_asyncio

if TYPE_CHECKING:
    from motor.core import AgnosticClient, AgnosticDatabase


async def init_mongo(url: str) -> AsyncIterator[AgnosticDatabase]:
    mongo_client: AgnosticClient = motor.motor_asyncio.AsyncIOMotorClient(url)
    mongo_default_db: AgnosticDatabase = mongo_client.get_default_database()
    yield mongo_default_db
    mongo_client.close
