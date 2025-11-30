from src.core_engine.utils.fuzzy_match import fuzzy_match_hard_config
from src.models.property_config import HardConfig


def test_exact_match_returns_true():
    reference = HardConfig(
        area_sqft=1200.0, bhk_type="3BHK", bedrooms=3, bathrooms=2, property_type="apartment"
    )

    candidate = HardConfig(
        area_sqft=1200.0, bhk_type="3BHK", bedrooms=3, bathrooms=2, property_type="apartment"
    )

    assert fuzzy_match_hard_config(reference, candidate, area_tolerance_percent=15.0) is True


def test_area_within_tolerance_returns_true():
    reference = HardConfig(
        area_sqft=1000.0, bhk_type="2BHK", bedrooms=2, bathrooms=2, property_type="apartment"
    )

    candidate = HardConfig(
        area_sqft=1100.0, bhk_type="2BHK", bedrooms=2, bathrooms=2, property_type="apartment"
    )

    assert fuzzy_match_hard_config(reference, candidate, area_tolerance_percent=15.0) is True


def test_area_outside_tolerance_returns_false():
    reference = HardConfig(
        area_sqft=1000.0, bhk_type="2BHK", bedrooms=2, bathrooms=2, property_type="apartment"
    )

    candidate = HardConfig(
        area_sqft=1200.0, bhk_type="2BHK", bedrooms=2, bathrooms=2, property_type="apartment"
    )

    assert fuzzy_match_hard_config(reference, candidate, area_tolerance_percent=15.0) is False


def test_different_bhk_type_returns_false():
    reference = HardConfig(
        area_sqft=1000.0, bhk_type="2BHK", bedrooms=2, bathrooms=2, property_type="apartment"
    )

    candidate = HardConfig(
        area_sqft=1000.0, bhk_type="3BHK", bedrooms=3, bathrooms=2, property_type="apartment"
    )

    assert fuzzy_match_hard_config(reference, candidate, area_tolerance_percent=15.0) is False


def test_different_bedrooms_returns_false():
    reference = HardConfig(
        area_sqft=1000.0, bhk_type="2BHK", bedrooms=2, bathrooms=2, property_type="apartment"
    )

    candidate = HardConfig(
        area_sqft=1000.0, bhk_type="2BHK", bedrooms=3, bathrooms=2, property_type="apartment"
    )

    assert fuzzy_match_hard_config(reference, candidate, area_tolerance_percent=15.0) is False


def test_different_bathrooms_returns_false():
    reference = HardConfig(
        area_sqft=1000.0, bhk_type="2BHK", bedrooms=2, bathrooms=2, property_type="apartment"
    )

    candidate = HardConfig(
        area_sqft=1000.0, bhk_type="2BHK", bedrooms=2, bathrooms=3, property_type="apartment"
    )

    assert fuzzy_match_hard_config(reference, candidate, area_tolerance_percent=15.0) is False


def test_different_property_type_returns_false():
    reference = HardConfig(
        area_sqft=1000.0, bhk_type="2BHK", bedrooms=2, bathrooms=2, property_type="apartment"
    )

    candidate = HardConfig(
        area_sqft=1000.0, bhk_type="2BHK", bedrooms=2, bathrooms=2, property_type="villa"
    )

    assert fuzzy_match_hard_config(reference, candidate, area_tolerance_percent=15.0) is False


def test_area_at_lower_boundary_returns_true():
    reference = HardConfig(
        area_sqft=1000.0, bhk_type="2BHK", bedrooms=2, bathrooms=2, property_type="apartment"
    )

    candidate = HardConfig(
        area_sqft=850.0, bhk_type="2BHK", bedrooms=2, bathrooms=2, property_type="apartment"
    )

    assert fuzzy_match_hard_config(reference, candidate, area_tolerance_percent=15.0) is True


def test_area_at_upper_boundary_returns_true():
    reference = HardConfig(
        area_sqft=1000.0, bhk_type="2BHK", bedrooms=2, bathrooms=2, property_type="apartment"
    )

    candidate = HardConfig(
        area_sqft=1150.0, bhk_type="2BHK", bedrooms=2, bathrooms=2, property_type="apartment"
    )

    assert fuzzy_match_hard_config(reference, candidate, area_tolerance_percent=15.0) is True
