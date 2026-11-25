import os
from typing import Any, Literal

from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection

DatabaseName = Literal["MyDatabase"]


class MongoService:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    client: AsyncMongoClient[dict[str, Any]] | None = None

    def _get_client(self) -> AsyncMongoClient[dict[str, Any]]:
        if self.client is None:
            url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
            self.client = AsyncMongoClient(url)
        return self.client

    async def init_service(self) -> None:
        self._get_client()
        await self.create_indexes()

    def get_collection(
        self,
        collection_name: str,
        database_name: DatabaseName = "MyDatabase",
    ) -> AsyncCollection[dict[str, Any]]:
        client = self._get_client()
        db = client.get_database(database_name)
        return db.get_collection(collection_name)

    async def create_indexes(self) -> None:
        pass

    async def close(self) -> None:
        if self.client is not None:
            await self.client.close()
            self.client = None
