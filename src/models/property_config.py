from pydantic import BaseModel
from typing import Dict


class HardConfig(BaseModel):
    area_sqft: float
    bhk_type: str
    bedrooms: int
    bathrooms: int
    property_type: str


class SoftConfig(BaseModel):
    furniture_items: list[str]
    appliances: list[str]
    amenities: list[str]

class Map(BaseModel):
    key: str
    value: str

class DynamicConfig(BaseModel):
    dynamic_map: Dict[str, Map] 
