from src.models.property_config import HardConfig


def fuzzy_match_hard_config(
    reference: HardConfig, candidate: HardConfig, area_tolerance_percent: float
) -> bool:
    if reference.bhk_type != candidate.bhk_type:
        return False

    if reference.bedrooms != candidate.bedrooms:
        return False

    if reference.bathrooms != candidate.bathrooms:
        return False

    if reference.property_type != candidate.property_type:
        return False

    tolerance = reference.area_sqft * (area_tolerance_percent / 100)
    lower_bound = reference.area_sqft - tolerance
    upper_bound = reference.area_sqft + tolerance

    return not (candidate.area_sqft < lower_bound or candidate.area_sqft > upper_bound)
