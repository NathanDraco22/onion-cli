from string import Template

mongo_service_template = Template("""import os
from typing import Literal, Any

from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection

DatabaseName = Literal["MyDatabase"]


class MongoService:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(MongoService, cls).__new__(cls)
        return cls.instance

    client: AsyncMongoClient[dict[str, Any]]

    async def init_service(self):
        url: str = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        self.client = AsyncMongoClient(url)
        await self.create_indexes()

    def get_collection(
        self,
        collection_name: str,
        database_name: DatabaseName = "MyDatabase",
    ) -> AsyncCollection[dict[str, Any]]:
        db = self.client.get_database(database_name)
        return db.get_collection(collection_name)

    async def create_indexes(self):
        pass

""")


def get_mongo_service_template() -> str:
    return mongo_service_template.template
