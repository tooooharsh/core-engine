import pytest
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from testcontainers.core.wait_strategies import (
    LogMessageWaitStrategy,
)
from testcontainers.mongodb import MongoDbContainer

from src.database.property_repository import PropertyRepository


@pytest.fixture(scope="session")
def mongo_container():
    container = MongoDbContainer("mongo:7.0").waiting_for(
        LogMessageWaitStrategy("Waiting for connections")
    )
    container.start()

    yield container
    container.stop()


@pytest_asyncio.fixture
async def mongo_client(mongo_container):
    client: AsyncIOMotorClient = AsyncIOMotorClient(mongo_container.get_connection_url())
    yield client
    client.close()


@pytest_asyncio.fixture
async def mongo_database(mongo_client):
    db = mongo_client["test_rentease"]
    yield db
    await mongo_client.drop_database("test_rentease")


@pytest_asyncio.fixture
async def property_repository(mongo_database):
    collection = mongo_database["properties"]
    return PropertyRepository(collection)
