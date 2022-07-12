from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator

import motor.motor_asyncio
from pymongo import ASCENDING, IndexModel

from .clients import MongoDatabaseClient

if TYPE_CHECKING:
    from motor.core import AgnosticClient, AgnosticDatabase


async def init_mongo(url: str) -> AsyncIterator[MongoDatabaseClient]:
    mongo_client: AgnosticClient = motor.motor_asyncio.AsyncIOMotorClient(url)
    mongo_default_db: AgnosticDatabase = mongo_client.get_default_database()
    await configure_db(mongo_default_db)
    db_client = MongoDatabaseClient(mongo_default_db)
    yield db_client
    mongo_client.close


async def configure_db(db_client: AgnosticDatabase) -> AgnosticDatabase:
    await create_indexes(db_client)
    return db_client


async def create_indexes(db_client: AgnosticDatabase) -> AgnosticDatabase:
    review_unique_index = IndexModel(
        keys=[("user_id", ASCENDING), ("film_id", ASCENDING)],
        name="review_film_user_unq",
        unique=True,
    )
    await db_client.reviews.create_indexes([review_unique_index])
    return db_client
