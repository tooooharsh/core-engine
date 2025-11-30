from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, HttpUrl

from src.models.property_config import HardConfig, SoftConfig

ChannelType = Literal["nobroker", "magicbrick"]


class PropertyListing(BaseModel):
    id: str
    channel: ChannelType
    channel_id: str
    title: str
    city: str
    locality: str
    society: str | None
    propertyType: str
    bedrooms: str
    bathrooms: int
    furnishing: str | None
    facing: str | None
    areaSqFt: float
    price: float
    deposit: float | None
    ownerName: str | None
    description: str | None
    latitude: float
    longitude: float
    postedDate: datetime
    url: str
    images: list[HttpUrl]
    landmarks: list[str]

    model_config = ConfigDict(from_attributes=True)


class Property(BaseModel):
    id: str
    hard_config: HardConfig
    soft_config: SoftConfig
    city: str
    locality: str
    latitude: float
    longitude: float
    current_rent: float | None

    model_config = ConfigDict(from_attributes=True)
