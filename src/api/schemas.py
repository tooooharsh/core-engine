from typing import Any

from pydantic import BaseModel


class HardConfigRequest(BaseModel):
    area_sqft: float
    bhk_type: str
    bedrooms: int
    bathrooms: int
    property_type: str


class SoftConfigRequest(BaseModel):
    furniture_items: list[str]
    appliances: list[str]
    amenities: list[str]


class PropertyCreateRequest(BaseModel):
    hard_config: HardConfigRequest
    soft_config: SoftConfigRequest
    city: str
    locality: str
    latitude: float
    longitude: float
    current_rent: float | None = None


class PropertyResponse(BaseModel):
    id: str
    hard_config: HardConfigRequest
    soft_config: SoftConfigRequest
    city: str
    locality: str
    latitude: float
    longitude: float
    current_rent: float | None


class PropertyAnalysisRequest(BaseModel):
    property_id: str
    radius_km: float = 2.0
    area_tolerance_percent: float = 15.0


class PropertyAnalysisResponse(BaseModel):
    property_id: str
    filtered_properties_count: int
    banding_result: dict[str, Any] | None
    iqr_analysis: dict[str, float] | None
