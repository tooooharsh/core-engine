from src.models.property_config import HardConfig, SoftConfig


def test_hard_config_creation():
    hard_config = HardConfig(
        area_sqft=1200.0, bhk_type="3BHK", bedrooms=3, bathrooms=2, property_type="apartment"
    )

    assert hard_config.area_sqft == 1200.0
    assert hard_config.bhk_type == "3BHK"
    assert hard_config.bedrooms == 3
    assert hard_config.bathrooms == 2
    assert hard_config.property_type == "apartment"


def test_soft_config_creation():
    soft_config = SoftConfig(
        furniture_items=["sofa", "bed", "dining_table"],
        appliances=["fridge", "ac", "washing_machine"],
        amenities=["parking", "gym"],
    )

    assert len(soft_config.furniture_items) == 3
    assert "sofa" in soft_config.furniture_items
    assert len(soft_config.appliances) == 3
    assert "fridge" in soft_config.appliances
    assert len(soft_config.amenities) == 2
    assert "parking" in soft_config.amenities


def test_soft_config_with_empty_lists():
    soft_config = SoftConfig(furniture_items=[], appliances=[], amenities=[])

    assert soft_config.furniture_items == []
    assert soft_config.appliances == []
    assert soft_config.amenities == []
