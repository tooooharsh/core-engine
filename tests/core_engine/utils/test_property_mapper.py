from datetime import datetime

from pydantic import HttpUrl

from src.core_engine.utils.property_mapper import map_listing_to_property
from src.models.property import PropertyListing


def test_map_fully_furnished_property():
    listing = PropertyListing(
        id="test1",
        channel="nobroker",
        channel_id="nb_123",
        title="Luxury 2BHK in Koramangala",
        city="Bangalore",
        locality="Koramangala",
        society="Prestige Heights",
        propertyType="apartment",
        bedrooms="2",
        bathrooms=2,
        furnishing="fully_furnished",
        facing="East",
        areaSqFt=1200.0,
        price=30000.0,
        deposit=90000.0,
        ownerName="John Doe",
        description="Beautiful 2BHK with all amenities",
        latitude=12.9352,
        longitude=77.6245,
        postedDate=datetime.now(),
        url="https://nobroker.com/test",
        images=[HttpUrl("https://example.com/img1.jpg")],
        landmarks=["Forum Mall", "Wipro Office"],
    )

    property_obj = map_listing_to_property(listing)

    assert property_obj.id == "test1"
    assert property_obj.hard_config.area_sqft == 1200.0
    assert property_obj.hard_config.bhk_type == "2BHK"
    assert property_obj.hard_config.bedrooms == 2
    assert property_obj.hard_config.bathrooms == 2
    assert property_obj.hard_config.property_type == "apartment"
    assert property_obj.city == "Bangalore"
    assert property_obj.locality == "Koramangala"
    assert property_obj.latitude == 12.9352
    assert property_obj.longitude == 77.6245
    assert property_obj.current_rent == 30000.0


def test_map_semi_furnished_property():
    listing = PropertyListing(
        id="test2",
        channel="magicbrick",
        channel_id="mb_456",
        title="Spacious 3BHK",
        city="Mumbai",
        locality="Andheri",
        society=None,
        propertyType="apartment",
        bedrooms="3",
        bathrooms=2,
        furnishing="semi_furnished",
        facing=None,
        areaSqFt=1500.0,
        price=45000.0,
        deposit=None,
        ownerName=None,
        description=None,
        latitude=19.1136,
        longitude=72.8697,
        postedDate=datetime.now(),
        url="https://magicbricks.com/test",
        images=[HttpUrl("https://example.com/img1.jpg")],
        landmarks=[],
    )

    property_obj = map_listing_to_property(listing)

    assert property_obj.hard_config.bhk_type == "3BHK"
    assert property_obj.hard_config.bedrooms == 3
    assert len(property_obj.soft_config.furniture_items) > 0
    assert len(property_obj.soft_config.appliances) > 0


def test_map_unfurnished_property():
    listing = PropertyListing(
        id="test3",
        channel="nobroker",
        channel_id="nb_789",
        title="Simple 1BHK",
        city="Pune",
        locality="Kothrud",
        society=None,
        propertyType="apartment",
        bedrooms="1",
        bathrooms=1,
        furnishing="unfurnished",
        facing=None,
        areaSqFt=600.0,
        price=12000.0,
        deposit=None,
        ownerName=None,
        description=None,
        latitude=18.5074,
        longitude=73.8077,
        postedDate=datetime.now(),
        url="https://nobroker.com/test3",
        images=[],
        landmarks=[],
    )

    property_obj = map_listing_to_property(listing)

    assert property_obj.hard_config.bhk_type == "1BHK"
    assert property_obj.soft_config.furniture_items == []
    assert property_obj.soft_config.appliances == []
    assert property_obj.soft_config.amenities == []


def test_map_property_with_no_furnishing_info():
    listing = PropertyListing(
        id="test4",
        channel="nobroker",
        channel_id="nb_999",
        title="2BHK apartment",
        city="Delhi",
        locality="Rohini",
        society=None,
        propertyType="apartment",
        bedrooms="2",
        bathrooms=2,
        furnishing=None,
        facing=None,
        areaSqFt=1000.0,
        price=25000.0,
        deposit=None,
        ownerName=None,
        description=None,
        latitude=28.7041,
        longitude=77.1025,
        postedDate=datetime.now(),
        url="https://nobroker.com/test4",
        images=[],
        landmarks=[],
    )

    property_obj = map_listing_to_property(listing)

    assert property_obj.soft_config.furniture_items == []
    assert property_obj.soft_config.appliances == []
    assert property_obj.soft_config.amenities == []


def test_bhk_type_extraction_from_bedrooms():
    listing = PropertyListing(
        id="test5",
        channel="nobroker",
        channel_id="nb_555",
        title="Property",
        city="Chennai",
        locality="T Nagar",
        society=None,
        propertyType="villa",
        bedrooms="4",
        bathrooms=3,
        furnishing=None,
        facing=None,
        areaSqFt=2000.0,
        price=60000.0,
        deposit=None,
        ownerName=None,
        description=None,
        latitude=13.0418,
        longitude=80.2341,
        postedDate=datetime.now(),
        url="https://nobroker.com/test5",
        images=[],
        landmarks=[],
    )

    property_obj = map_listing_to_property(listing)

    assert property_obj.hard_config.bhk_type == "4BHK"
    assert property_obj.hard_config.property_type == "villa"


def test_map_property_preserves_id():
    listing = PropertyListing(
        id="unique_id_123",
        channel="nobroker",
        channel_id="nb_abc",
        title="Test Property",
        city="Bangalore",
        locality="HSR Layout",
        society=None,
        propertyType="apartment",
        bedrooms="2",
        bathrooms=2,
        furnishing=None,
        facing=None,
        areaSqFt=1100.0,
        price=28000.0,
        deposit=None,
        ownerName=None,
        description=None,
        latitude=12.9121,
        longitude=77.6446,
        postedDate=datetime.now(),
        url="https://nobroker.com/test",
        images=[],
        landmarks=[],
    )

    property_obj = map_listing_to_property(listing)

    assert property_obj.id == "unique_id_123"
