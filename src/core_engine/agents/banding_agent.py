from typing import cast

from langchain_anthropic import ChatAnthropic
from pydantic import BaseModel, Field, SecretStr

from src.models.property import Property


class BandingResult(BaseModel):
    bands: dict[str, list[str]] = Field(description="Property IDs grouped by band (L1-L5)")
    parameters_used: list[str] = Field(description="List of parameters used for banding")
    parameters_rationale: str = Field(description="Explanation of why these parameters were chosen")
    new_property_band: str = Field(description="Band assigned to the new property (L1-L5)")
    confidence_score: float = Field(description="Confidence score between 0 and 1")


class PropertyBandingAgent:
    def __init__(self, anthropic_api_key: str):
        self.llm = ChatAnthropic(
            model_name="claude-3-5-sonnet-20241022",
            temperature=0.5,
            api_key=SecretStr(anthropic_api_key),
        )

    def band_properties(
        self,
        new_property: Property,
        similar_properties: list[Property],
        parameter_hints: list[str] | None = None,
    ) -> BandingResult:
        if parameter_hints is None:
            parameter_hints = ["furnishing_level", "rent_per_sqft", "amenities_count"]

        structured_llm = self.llm.with_structured_output(BandingResult)

        prompt = self._build_prompt(new_property, similar_properties, parameter_hints)

        result = structured_llm.invoke(prompt)

        return cast(BandingResult, result)

    def _build_prompt(
        self, new_property: Property, similar_properties: list[Property], parameter_hints: list[str]
    ) -> str:
        prompt = f"""You are a property analysis expert. Your task is to categorize properties \
into 5 bands (L1 to L5) based on their features and market positioning.

L5 = Best/Premium properties
L4 = High-quality properties
L3 = Mid-range properties
L2 = Basic properties
L1 = Minimal/Entry-level properties

Parameter Hints (you can use these or discover better ones):
{", ".join(parameter_hints)}

Similar Properties to Analyze:
"""

        for prop in similar_properties:
            furniture = (
                ", ".join(prop.soft_config.furniture_items)
                if prop.soft_config.furniture_items
                else "None"
            )
            appliances = (
                ", ".join(prop.soft_config.appliances) if prop.soft_config.appliances else "None"
            )
            amenities = (
                ", ".join(prop.soft_config.amenities) if prop.soft_config.amenities else "None"
            )
            prompt += f"""
Property ID: {prop.id}
- Furniture: {furniture}
- Appliances: {appliances}
- Amenities: {amenities}
- Current Rent: {prop.current_rent if prop.current_rent else "Not set"}
- Area: {prop.hard_config.area_sqft} sqft
"""

        new_furniture = (
            ", ".join(new_property.soft_config.furniture_items)
            if new_property.soft_config.furniture_items
            else "None"
        )
        new_appliances = (
            ", ".join(new_property.soft_config.appliances)
            if new_property.soft_config.appliances
            else "None"
        )
        new_amenities = (
            ", ".join(new_property.soft_config.amenities)
            if new_property.soft_config.amenities
            else "None"
        )

        prompt += f"""

New Property to Classify:
Property ID: {new_property.id}
- Furniture: {new_furniture}
- Appliances: {new_appliances}
- Amenities: {new_amenities}
- Area: {new_property.hard_config.area_sqft} sqft

Task:
1. Analyze the similar properties and categorize them into bands L1-L5
2. Determine which parameters are most relevant for categorization
3. Place the new property into the appropriate band
4. Provide confidence score and rationale

Return a structured response with:
- bands: Dictionary mapping band names to lists of property IDs
- parameters_used: List of parameters you used
- parameters_rationale: Brief explanation of your categorization logic
- new_property_band: The band for the new property
- confidence_score: Your confidence (0-1)
"""

        return prompt
