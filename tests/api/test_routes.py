import pytest
from httpx import ASGITransport, AsyncClient

from src.api.dependencies import get_property_repository
from src.api.main import app
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


@pytest.mark.asyncio
async def test_health_check():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_create_property(property_repository):
    app.dependency_overrides[get_property_repository] = lambda: property_repository

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/properties",
            json={
                "hard_config": {
                    "area_sqft": 1200.0,
                    "bhk_type": "2BHK",
                    "bedrooms": 2,
                    "bathrooms": 2,
                    "property_type": "apartment",
                },
                "soft_config": {
                    "furniture_items": ["sofa", "bed"],
                    "appliances": ["fridge"],
                    "amenities": ["parking"],
                },
                "city": "Bangalore",
                "locality": "Koramangala",
                "latitude": 12.9352,
                "longitude": 77.6245,
                "current_rent": 30000.0,
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["city"] == "Bangalore"
        assert data["hard_config"]["area_sqft"] == 1200.0

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_property(property_repository, test_property):
    await property_repository.create(test_property)

    app.dependency_overrides[get_property_repository] = lambda: property_repository

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/properties/test_prop_1")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "test_prop_1"
        assert data["city"] == "Bangalore"

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_property_not_found(property_repository):
    app.dependency_overrides[get_property_repository] = lambda: property_repository

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/properties/non_existent")

        assert response.status_code == 404

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_list_properties(property_repository, test_property):
    await property_repository.create(test_property)

    app.dependency_overrides[get_property_repository] = lambda: property_repository

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/properties")

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        ids = [p["id"] for p in data]
        assert "test_prop_1" in ids

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_list_properties_by_city(property_repository, test_property):
    await property_repository.create(test_property)

    app.dependency_overrides[get_property_repository] = lambda: property_repository

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/properties?city=Bangalore")

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert all(p["city"] == "Bangalore" for p in data)

    app.dependency_overrides.clear()
