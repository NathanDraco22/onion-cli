from typing import Self

from services.mongo_service import MongoService


class BaseMongoCollection:
    collection_name: str = ""
    _instance: "BaseMongoCollection | None" = None

    def __init__(self) -> None:
        mongo_service = MongoService()
        self._collection = mongo_service.get_collection(self.collection_name)

    @classmethod
    def get_instance(cls) -> Self:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance  # type: ignore
