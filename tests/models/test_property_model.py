from src.models.property import Property
from src.models.property_config import HardConfig, SoftConfig


def test_property_creation_with_configs():
    hard_config = HardConfig(
        area_sqft=1200.0, bhk_type="3BHK", bedrooms=3, bathrooms=2, property_type="apartment"
    )

    soft_config = SoftConfig(
        furniture_items=["sofa", "bed"], appliances=["fridge", "ac"], amenities=["parking"]
    )

    property_obj = Property(
        id="test_prop_1",
        hard_config=hard_config,
        soft_config=soft_config,
        city="Bangalore",
        locality="Koramangala",
        latitude=12.9352,
        longitude=77.6245,
        current_rent=None,
    )

    assert property_obj.id == "test_prop_1"
    assert property_obj.hard_config.area_sqft == 1200.0
    assert property_obj.hard_config.bhk_type == "3BHK"
    assert len(property_obj.soft_config.furniture_items) == 2
    assert property_obj.city == "Bangalore"
    assert property_obj.current_rent is None


def test_property_with_rent():
    hard_config = HardConfig(
        area_sqft=1000.0, bhk_type="2BHK", bedrooms=2, bathrooms=2, property_type="apartment"
    )

    soft_config = SoftConfig(furniture_items=[], appliances=[], amenities=[])

    property_obj = Property(
        id="test_prop_2",
        hard_config=hard_config,
        soft_config=soft_config,
        city="Mumbai",
        locality="Andheri",
        latitude=19.1136,
        longitude=72.8697,
        current_rent=25000.0,
    )

    assert property_obj.current_rent == 25000.0
