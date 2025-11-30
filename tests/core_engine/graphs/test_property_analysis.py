import pytest

from src.core_engine.graphs.property_analysis import (
    analyze_nearby_properties,
)
from tests.fixtures import create_test_properties


@pytest.fixture
def properties():
    return create_test_properties()


def test_property_analysis_workflow(properties):
    reference = properties[0]  # Property at (0, 0)
    result = analyze_nearby_properties(properties, reference)

    # Verify structure
    assert "filtered_properties" in result
    assert "price_analysis" in result

    # Verify filtering
    filtered = result["filtered_properties"]
    assert len(filtered) == 2  # Two properties within 2km
    assert all(p.id in ["near1", "near2"] for p in filtered)

    # Verify price analysis
    analysis = result["price_analysis"]
    assert analysis["count"] == 2
    assert analysis["average_price"] == 1050000.0  # (1200000 + 900000) / 2
    assert analysis["min_price"] == 900000.0
    assert analysis["max_price"] == 1200000.0


def test_property_analysis_custom_radius(properties):
    reference = properties[0]
    result = analyze_nearby_properties(properties, reference, radius_km=4.0)

    # Should include all properties except reference
    filtered = result["filtered_properties"]
    assert len(filtered) == 3

    # Verify all non-reference properties are included
    assert all(p.id != reference.id for p in filtered)
    assert all(p.id in ["near1", "near2", "far1"] for p in filtered)


def test_property_analysis_empty_result(properties):
    # Create a reference property far from others
    far_reference = create_test_properties()[0]
    far_reference.latitude = 1.0  # Move it far away

    result = analyze_nearby_properties(properties, far_reference)

    assert len(result["filtered_properties"]) == 0
    assert result["price_analysis"]["count"] == 0
    assert result["price_analysis"]["average_price"] == 0
