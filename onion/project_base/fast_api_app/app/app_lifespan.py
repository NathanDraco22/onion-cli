from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.services_initializer import close_services, init_services


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_services()
    yield
    await close_services()
