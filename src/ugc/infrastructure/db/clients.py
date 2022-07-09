from motor.core import AgnosticCollection, AgnosticDatabase
from pymongo import results


class MongoDatabaseClient:
    """Клиент для работы с базой данной из MongoDB."""

    collection_cache: dict[tuple, "MongoCollectionClient"] = {}

    def __init__(self, db_client: AgnosticDatabase) -> None:
        assert isinstance(db_client, AgnosticDatabase)
        self._client = db_client

    def __getattr__(self, name: str) -> "MongoCollectionClient":
        if name.startswith("_"):
            raise AttributeError(f"Cannot access private collection <{name}>")
        return self[name]

    def __getitem__(self, name: str) -> "MongoCollectionClient":
        mongo_client = self._client.__getattr__(name)
        return self._get_collection_client(name, mongo_client)

    def _get_collection_client(self, name: str, mongo_client: AgnosticCollection) -> "MongoCollectionClient":
        cache_key = ("MongoCollectionClient", name, self.__module__)
        cached_client = self.collection_cache.get(cache_key)
        if cached_client:
            return cached_client
        new_client = MongoCollectionClient(collection_client=mongo_client)
        return new_client


class MongoCollectionClient:
    """Клиент для работы с коллекций документов MongoDB."""

    def __init__(self, collection_client: AgnosticCollection) -> None:
        assert isinstance(collection_client, AgnosticCollection)
        self._client = collection_client

    async def insert_one(self, document: dict) -> results.InsertOneResult:
        """Добавление одного документа в коллекцию."""
        result = await self._client.insert_one(document)
        return result
