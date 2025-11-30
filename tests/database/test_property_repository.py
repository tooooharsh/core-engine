import pytest

from src.models.property import Property
from src.models.property_config import HardConfig, SoftConfig


@pytest.fixture
def test_property():
    return Property(
        id="test_prop_1",
        hard_config=HardConfig(
            area_sqft=1200.0, bhk_type="2BHK", bedrooms=2, bathrooms=2, property_type="apartment"
        ),
        soft_config=SoftConfig(
            furniture_items=["sofa", "bed"], appliances=["fridge"], amenities=["parking"]
        ),
        city="Bangalore",
        locality="Koramangala",
        latitude=12.9352,
        longitude=77.6245,
        current_rent=30000.0,
    )


@pytest.fixture
def another_property():
    return Property(
        id="test_prop_2",
        hard_config=HardConfig(
            area_sqft=1000.0, bhk_type="2BHK", bedrooms=2, bathrooms=2, property_type="apartment"
        ),
        soft_config=SoftConfig(furniture_items=[], appliances=[], amenities=[]),
        city="Bangalore",
        locality="HSR",
        latitude=12.9121,
        longitude=77.6446,
        current_rent=25000.0,
    )


@pytest.mark.asyncio
async def test_create_property(property_repository, test_property):
    result = await property_repository.create(test_property)

    assert result.id == test_property.id
    assert result.hard_config.area_sqft == 1200.0
    assert result.city == "Bangalore"


@pytest.mark.asyncio
async def test_get_property_by_id(property_repository, test_property):
    await property_repository.create(test_property)

    result = await property_repository.get_by_id("test_prop_1")

    assert result is not None
    assert result.id == "test_prop_1"
    assert result.hard_config.area_sqft == 1200.0
    assert result.hard_config.bhk_type == "2BHK"
    assert result.city == "Bangalore"


@pytest.mark.asyncio
async def test_get_property_by_id_not_found(property_repository):
    result = await property_repository.get_by_id("non_existent")

    assert result is None


@pytest.mark.asyncio
async def test_get_all_properties(property_repository, test_property, another_property):
    await property_repository.create(test_property)
    await property_repository.create(another_property)

    result = await property_repository.get_all()

    assert len(result) == 2
    ids = [p.id for p in result]
    assert "test_prop_1" in ids
    assert "test_prop_2" in ids


@pytest.mark.asyncio
async def test_get_properties_by_city(property_repository, test_property, another_property):
    await property_repository.create(test_property)
    await property_repository.create(another_property)

    result = await property_repository.get_by_city("Bangalore")

    assert len(result) == 2
    assert all(p.city == "Bangalore" for p in result)


@pytest.mark.asyncio
async def test_update_property(property_repository, test_property):
    await property_repository.create(test_property)

    test_property.current_rent = 35000.0
    result = await property_repository.update(test_property)

    assert result.current_rent == 35000.0

    fetched = await property_repository.get_by_id("test_prop_1")
    assert fetched.current_rent == 35000.0


@pytest.mark.asyncio
async def test_delete_property(property_repository, test_property):
    await property_repository.create(test_property)

    result = await property_repository.delete("test_prop_1")

    assert result is True

    fetched = await property_repository.get_by_id("test_prop_1")
    assert fetched is None


@pytest.mark.asyncio
async def test_delete_property_not_found(property_repository):
    result = await property_repository.delete("non_existent")

    assert result is False
