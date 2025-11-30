from unittest.mock import Mock, patch

import pytest

from src.core_engine.agents.banding_agent import BandingResult, PropertyBandingAgent
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


def test_banding_agent_initialization():
    agent = PropertyBandingAgent(anthropic_api_key="test_key")
    assert agent is not None


@patch("src.core_engine.agents.banding_agent.ChatAnthropic")
def test_banding_agent_categorizes_properties(mock_chat_anthropic, test_properties, new_property):
    mock_llm = Mock()
    mock_chat_anthropic.return_value = mock_llm

    mock_response = BandingResult(
        bands={"L5": ["prop1"], "L3": ["prop2"], "L1": ["prop3"]},
        parameters_used=["furnishing_score", "appliances_count", "rent_per_sqft"],
        parameters_rationale="Categorized based on furnishing level and amenities",
        new_property_band="L4",
        confidence_score=0.85,
    )

    mock_llm.with_structured_output.return_value.invoke.return_value = mock_response

    agent = PropertyBandingAgent(anthropic_api_key="test_key")
    result = agent.band_properties(new_property, test_properties)

    assert isinstance(result, BandingResult)
    assert result.new_property_band == "L4"
    assert "L5" in result.bands
    assert "L3" in result.bands
    assert "L1" in result.bands
    assert len(result.parameters_used) > 0
    assert result.confidence_score > 0


@patch("src.core_engine.agents.banding_agent.ChatAnthropic")
def test_banding_agent_with_minimal_parameters(mock_chat_anthropic, test_properties, new_property):
    mock_llm = Mock()
    mock_chat_anthropic.return_value = mock_llm

    mock_response = BandingResult(
        bands={"L5": ["prop1"], "L2": ["prop2", "prop3"]},
        parameters_used=["furnishing_level"],
        parameters_rationale="Simple categorization based on furnishing",
        new_property_band="L3",
        confidence_score=0.75,
    )

    mock_llm.with_structured_output.return_value.invoke.return_value = mock_response

    agent = PropertyBandingAgent(anthropic_api_key="test_key")
    result = agent.band_properties(
        new_property, test_properties, parameter_hints=["furnishing_level"]
    )

    assert result.new_property_band == "L3"
    assert "furnishing_level" in result.parameters_used


@patch("src.core_engine.agents.banding_agent.ChatAnthropic")
def test_banding_result_structure(mock_chat_anthropic, test_properties, new_property):
    mock_llm = Mock()
    mock_chat_anthropic.return_value = mock_llm

    mock_response = BandingResult(
        bands={"L5": ["prop1"], "L3": ["prop2"], "L1": ["prop3"]},
        parameters_used=["furnishing_score", "rent_per_sqft"],
        parameters_rationale="Based on furnishing quality and market positioning",
        new_property_band="L3",
        confidence_score=0.9,
    )

    mock_llm.with_structured_output.return_value.invoke.return_value = mock_response

    agent = PropertyBandingAgent(anthropic_api_key="test_key")
    result = agent.band_properties(new_property, test_properties)

    assert hasattr(result, "bands")
    assert hasattr(result, "parameters_used")
    assert hasattr(result, "parameters_rationale")
    assert hasattr(result, "new_property_band")
    assert hasattr(result, "confidence_score")
    assert isinstance(result.bands, dict)
    assert isinstance(result.parameters_used, list)
    assert isinstance(result.parameters_rationale, str)
    assert isinstance(result.new_property_band, str)
    assert isinstance(result.confidence_score, float)
