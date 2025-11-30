from datetime import datetime

from pydantic import HttpUrl

from src.models.property import PropertyListing


def create_test_property(
    _id: str, latitude: float, longitude: float, price: float = 1000000.0
) -> PropertyListing:
    return PropertyListing(
        id=_id,
        channel="nobroker",
        channel_id=f"test_{_id}",
        title=f"Test Property {_id}",
        city="Test City",
        locality="Test Locality",
        society=None,  # Optional field
        propertyType="apartment",
        bedrooms="2",
        bathrooms=2,
        furnishing=None,  # Optional field
        facing=None,  # Optional field
        areaSqFt=1000.0,
        price=price,
        deposit=None,  # Optional field
        ownerName=None,  # Optional field
        description=None,  # Optional field
        latitude=latitude,
        longitude=longitude,
        postedDate=datetime.now(),
        url="https://example.com",
        images=[HttpUrl("https://example.com/img1.jpg")],
        landmarks=["Test Landmark"],
    )


def create_test_properties() -> list[PropertyListing]:
    """Creates a set of test properties with known locations and prices"""
    return [
        create_test_property("ref", 0.0, 0.0, 1000000.0),
        create_test_property("near1", 0.01, 0.01, 1200000.0),
        create_test_property("far1", 0.02, 0.02, 800000.0),
        create_test_property("near2", -0.01, -0.01, 900000.0),
    ]
