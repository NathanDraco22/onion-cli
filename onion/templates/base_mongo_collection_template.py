from string import Template


base_mongo_collection_template = Template(
    """from typing import TypeVar, Type

from services import MongoService


T = TypeVar("T", bound="BaseMongoCollection")


class BaseMongoCollection:
    collection_name: str = ""
    _instance: "BaseMongoCollection|None" = None

    def __init__(self) -> None:
        mongo_service = MongoService()
        self._collection = mongo_service.get_collection(self.collection_name)

    @classmethod
    def get_instance(cls: Type[T], db_name: str | None = None) -> T:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
"""
)


def get_base_mongo_collection_template() -> str:
    return base_mongo_collection_template.template
