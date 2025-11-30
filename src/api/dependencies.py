import os

from motor.motor_asyncio import AsyncIOMotorClient

from src.database.property_repository import PropertyRepository

mongo_client = None
database = None


def get_mongo_client():
    global mongo_client
    if mongo_client is None:
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        mongo_client = AsyncIOMotorClient(mongodb_url)
    return mongo_client


def get_database():
    global database
    if database is None:
        client = get_mongo_client()
        db_name = os.getenv("MONGODB_DATABASE", "rentease")
        database = client[db_name]
    return database


def get_property_repository() -> PropertyRepository:
    db = get_database()
    collection = db["properties"]
    return PropertyRepository(collection)


def get_anthropic_api_key() -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
    return api_key
