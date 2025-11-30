import uuid

from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies import get_property_repository
from src.api.schemas import (
    HardConfigRequest,
    PropertyAnalysisRequest,
    PropertyAnalysisResponse,
    PropertyCreateRequest,
    PropertyResponse,
    SoftConfigRequest,
)
from src.core_engine.graphs.property_banding_workflow import analyze_property_with_banding
from src.database.property_repository import PropertyRepository
from src.models.property import Property
from src.models.property_config import HardConfig, SoftConfig

router = APIRouter(prefix="/api/v1", tags=["properties"])


@router.post("/properties", response_model=PropertyResponse, status_code=201)
async def create_property(
    request: PropertyCreateRequest,
    repository: PropertyRepository = Depends(get_property_repository),
):
    property_obj = Property(
        id=str(uuid.uuid4()),
        hard_config=HardConfig(**request.hard_config.model_dump()),
        soft_config=SoftConfig(**request.soft_config.model_dump()),
        city=request.city,
        locality=request.locality,
        latitude=request.latitude,
        longitude=request.longitude,
        current_rent=request.current_rent,
    )

    created_property = await repository.create(property_obj)

    return PropertyResponse(
        id=created_property.id,
        hard_config=request.hard_config,
        soft_config=request.soft_config,
        city=created_property.city,
        locality=created_property.locality,
        latitude=created_property.latitude,
        longitude=created_property.longitude,
        current_rent=created_property.current_rent,
    )


@router.get("/properties/{property_id}", response_model=PropertyResponse)
async def get_property(
    property_id: str, repository: PropertyRepository = Depends(get_property_repository)
):
    property_obj = await repository.get_by_id(property_id)

    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")

    return PropertyResponse(
        id=property_obj.id,
        hard_config=HardConfigRequest(**property_obj.hard_config.model_dump()),
        soft_config=SoftConfigRequest(**property_obj.soft_config.model_dump()),
        city=property_obj.city,
        locality=property_obj.locality,
        latitude=property_obj.latitude,
        longitude=property_obj.longitude,
        current_rent=property_obj.current_rent,
    )


@router.get("/properties", response_model=list[PropertyResponse])
async def list_properties(
    city: str | None = None, repository: PropertyRepository = Depends(get_property_repository)
):
    if city:
        properties = await repository.get_by_city(city)
    else:
        properties = await repository.get_all()

    return [
        PropertyResponse(
            id=prop.id,
            hard_config=HardConfigRequest(**prop.hard_config.model_dump()),
            soft_config=SoftConfigRequest(**prop.soft_config.model_dump()),
            city=prop.city,
            locality=prop.locality,
            latitude=prop.latitude,
            longitude=prop.longitude,
            current_rent=prop.current_rent,
        )
        for prop in properties
    ]


@router.post("/properties/analyze", response_model=PropertyAnalysisResponse)
async def analyze_property(
    request: PropertyAnalysisRequest,
    repository: PropertyRepository = Depends(get_property_repository),
):
    property_obj = await repository.get_by_id(request.property_id)

    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")

    all_properties = await repository.get_by_city(property_obj.city)

    result = analyze_property_with_banding(
        new_property=property_obj,
        all_properties=all_properties,
        radius_km=request.radius_km,
        area_tolerance_percent=request.area_tolerance_percent,
    )

    return PropertyAnalysisResponse(
        property_id=request.property_id,
        filtered_properties_count=len(result["filtered_properties"]),
        banding_result=result["banding_result"],
        iqr_analysis=result["iqr_analysis"],
    )
