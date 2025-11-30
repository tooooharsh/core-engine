from unittest.mock import Mock, patch

import pytest

from src.core_engine.agents.banding_agent import BandingResult
from src.core_engine.graphs.property_banding_workflow import analyze_property_with_banding
from src.models.property import Property
from src.models.property_config import HardConfig, SoftConfig


@pytest.fixture
def test_properties():
    properties = []
    base_hard = HardConfig(
        area_sqft=1000.0, bhk_type="2BHK", bedrooms=2, bathrooms=2, property_type="apartment"
    )

    prop1 = Property(
        id="prop1",
        hard_config=base_hard,
        soft_config=SoftConfig(
            furniture_items=["sofa", "bed", "dining_table", "wardrobe"],
            appliances=["fridge", "ac", "washing_machine", "tv"],
            amenities=["parking", "gym", "security"],
        ),
        city="Bangalore",
        locality="Koramangala",
        latitude=12.9352,
        longitude=77.6245,
        current_rent=35000.0,
    )

    prop2 = Property(
        id="prop2",
        hard_config=base_hard,
        soft_config=SoftConfig(
            furniture_items=["bed", "wardrobe"], appliances=["fridge"], amenities=["parking"]
        ),
        city="Bangalore",
        locality="Koramangala",
        latitude=12.9362,
        longitude=77.6255,
        current_rent=22000.0,
    )

    prop3 = Property(
        id="prop3",
        hard_config=base_hard,
        soft_config=SoftConfig(furniture_items=[], appliances=[], amenities=[]),
        city="Bangalore",
        locality="Koramangala",
        latitude=12.9372,
        longitude=77.6265,
        current_rent=18000.0,
    )

    properties.extend([prop1, prop2, prop3])
    return properties


@pytest.fixture
def new_property():
    return Property(
        id="new_prop",
        hard_config=HardConfig(
            area_sqft=1000.0, bhk_type="2BHK", bedrooms=2, bathrooms=2, property_type="apartment"
        ),
        soft_config=SoftConfig(
            furniture_items=["sofa", "bed", "dining_table"],
            appliances=["fridge", "ac"],
            amenities=["parking"],
        ),
        city="Bangalore",
        locality="Koramangala",
        latitude=12.9382,
        longitude=77.6275,
        current_rent=None,
    )


@patch("src.core_engine.agents.banding_agent.ChatAnthropic")
def test_property_banding_workflow(mock_chat_anthropic, test_properties, new_property):
    mock_llm = Mock()
    mock_chat_anthropic.return_value = mock_llm

    mock_banding_response = BandingResult(
        bands={"L5": ["prop1"], "L3": ["prop2"], "L1": ["prop3"]},
        parameters_used=["furnishing_score", "rent_per_sqft"],
        parameters_rationale="Categorized based on furnishing and rent",
        new_property_band="L3",
        confidence_score=0.85,
    )

    mock_llm.with_structured_output.return_value.invoke.return_value = mock_banding_response

    result = analyze_property_with_banding(
        new_property=new_property,
        all_properties=test_properties,
        radius_km=2.0,
        area_tolerance_percent=15.0,
    )

    assert "filtered_properties" in result
    assert "banding_result" in result
    assert "iqr_analysis" in result

    assert result["banding_result"]["new_property_band"] == "L3"
    assert "recommended_min" in result["iqr_analysis"]
    assert "recommended_max" in result["iqr_analysis"]


@patch("src.core_engine.agents.banding_agent.ChatAnthropic")
def test_workflow_with_no_similar_properties(mock_chat_anthropic, new_property):
    result = analyze_property_with_banding(
        new_property=new_property, all_properties=[], radius_km=2.0, area_tolerance_percent=15.0
    )

    assert result["filtered_properties"] == []
    assert result["banding_result"] is None
    assert result["iqr_analysis"] is None
