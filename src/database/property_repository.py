from motor.motor_asyncio import AsyncIOMotorCollection

from src.models.property import Property


class PropertyRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create(self, property_obj: Property) -> Property:
        property_dict = property_obj.model_dump()
        await self.collection.insert_one(property_dict)
        return property_obj

    async def get_by_id(self, property_id: str) -> Property | None:
        doc = await self.collection.find_one({"id": property_id})
        if doc:
            doc.pop("_id", None)
            return Property(**doc)
        return None

    async def get_all(self) -> list[Property]:
        cursor = self.collection.find({})
        docs = await cursor.to_list(length=None)
        properties = []
        for doc in docs:
            doc.pop("_id", None)
            properties.append(Property(**doc))
        return properties

    async def get_by_city(self, city: str) -> list[Property]:
        cursor = self.collection.find({"city": city})
        docs = await cursor.to_list(length=None)
        properties = []
        for doc in docs:
            doc.pop("_id", None)
            properties.append(Property(**doc))
        return properties

    async def update(self, property_obj: Property) -> Property:
        property_dict = property_obj.model_dump()
        await self.collection.replace_one({"id": property_obj.id}, property_dict)
        return property_obj

    async def delete(self, property_id: str) -> bool:
        result = await self.collection.delete_one({"id": property_id})
        return result.deleted_count > 0
