import pytest

from src.core_engine.agents.property_agents import PriceAnalyzerTool, PropertyFilterTool
from tests.fixtures import create_test_properties


@pytest.fixture
def properties():
    return create_test_properties()


@pytest.fixture
def property_filter():
    return PropertyFilterTool()


@pytest.fixture
def price_analyzer():
    return PriceAnalyzerTool()


def test_property_filter_within_radius(property_filter, properties):
    reference = properties[0]  # Property at (0, 0)
    filtered = property_filter._run(properties, reference)

    # Should only include properties within 2km (the two near properties)
    assert len(filtered) == 2
    assert all(p.id in ["near1", "near2"] for p in filtered)


def test_property_filter_custom_radius(property_filter, properties):
    reference = properties[0]
    filtered = property_filter._run(properties, reference, radius_km=4.0)

    # Should include all properties (they're all within 4km)
    assert len(filtered) == 3  # All except reference property


def test_property_filter_excludes_reference(property_filter, properties):
    reference = properties[0]
    filtered = property_filter._run(properties, reference)

    # Reference property should not be in filtered list
    assert all(p.id != reference.id for p in filtered)


def test_price_analyzer_basic(price_analyzer, properties):
    analysis = price_analyzer._run(properties)

    assert analysis["count"] == 4
    assert analysis["average_price"] == 975000.0  # (1000000 + 1200000 + 800000 + 900000) / 4
    assert analysis["min_price"] == 800000.0
    assert analysis["max_price"] == 1200000.0


def test_price_analyzer_empty_list(price_analyzer):
    analysis = price_analyzer._run([])

    assert analysis["count"] == 0
    assert analysis["average_price"] == 0
