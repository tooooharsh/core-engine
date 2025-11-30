from src.models.property import Property, PropertyListing
from src.models.property_config import HardConfig, SoftConfig


def extract_bhk_type(bedrooms: str) -> str:
    return f"{bedrooms}BHK"


def extract_soft_config_from_furnishing(furnishing: str | None) -> SoftConfig:
    if furnishing is None or furnishing.lower() == "unfurnished":
        return SoftConfig(furniture_items=[], appliances=[], amenities=[])

    if furnishing.lower() == "semi_furnished":
        return SoftConfig(furniture_items=["bed", "wardrobe"], appliances=["fridge"], amenities=[])

    if furnishing.lower() == "fully_furnished":
        return SoftConfig(
            furniture_items=["sofa", "bed", "dining_table", "wardrobe"],
            appliances=["fridge", "ac", "washing_machine", "tv"],
            amenities=["parking"],
        )

    return SoftConfig(furniture_items=[], appliances=[], amenities=[])


def map_listing_to_property(listing: PropertyListing) -> Property:
    hard_config = HardConfig(
        area_sqft=listing.areaSqFt,
        bhk_type=extract_bhk_type(listing.bedrooms),
        bedrooms=int(listing.bedrooms),
        bathrooms=listing.bathrooms,
        property_type=listing.propertyType,
    )

    soft_config = extract_soft_config_from_furnishing(listing.furnishing)

    property_obj = Property(
        id=listing.id,
        hard_config=hard_config,
        soft_config=soft_config,
        city=listing.city,
        locality=listing.locality,
        latitude=listing.latitude,
        longitude=listing.longitude,
        current_rent=listing.price,
    )

    return property_obj


def map_listings_to_properties(listings: list[PropertyListing]) -> list[Property]:
    return [map_listing_to_property(listing) for listing in listings]
