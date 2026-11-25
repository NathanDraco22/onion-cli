import os

from services import MongoService


async def init_services() -> None:
    if os.getenv("MONGO_URL"):
        await MongoService().init_service()


async def close_services() -> None:
    await MongoService().close()
