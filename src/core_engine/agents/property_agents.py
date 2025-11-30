from typing import Any

from langchain.tools import BaseTool
from pydantic import BaseModel, ConfigDict, Field

from src.core_engine.utils.geo import calculate_distance_km
from src.models.property import PropertyListing


class PropertyFilterInput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    properties: list[PropertyListing] = Field(
        ..., description="List of property listings to filter"
    )
    reference_property: PropertyListing = Field(
        ..., description="Reference property to calculate distance from"
    )
    radius_km: float = Field(default=2.0, description="Radius in kilometers to filter properties")


class PropertyFilterTool(BaseTool):
    name: str = "property_filter_tool"
    description: str = "Filters properties within a specified radius of a reference property"
    args_schema: type[BaseModel] = PropertyFilterInput

    def _run(
        self,
        properties: list[PropertyListing],
        reference_property: PropertyListing,
        radius_km: float = 2.0,
    ) -> list[PropertyListing]:
        filtered_properties = []

        for prop in properties:
            distance = calculate_distance_km(
                reference_property.latitude,
                reference_property.longitude,
                prop.latitude,
                prop.longitude,
            )

            if distance <= radius_km and prop.id != reference_property.id:
                filtered_properties.append(prop)

        return filtered_properties

    async def _arun(
        self,
        properties: list[PropertyListing],
        reference_property: PropertyListing,
        radius_km: float = 2.0,
    ) -> list[PropertyListing]:
        return self._run(properties, reference_property, radius_km)


class PriceAnalyzerTool(BaseTool):
    name: str = "price_analyzer_tool"
    description: str = "Calculates average price for a list of properties"

    def _run(self, properties: list[PropertyListing]) -> dict[str, Any]:
        if not properties:
            return {"average_price": 0, "count": 0}

        total_price = sum(prop.price for prop in properties)
        avg_price = total_price / len(properties)

        return {
            "average_price": avg_price,
            "count": len(properties),
            "min_price": min(prop.price for prop in properties),
            "max_price": max(prop.price for prop in properties),
        }

    async def _arun(self, properties: list[PropertyListing]) -> dict[str, Any]:
        return self._run(properties)
