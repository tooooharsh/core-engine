from typing import Any, TypedDict

from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.api.dependencies import get_anthropic_api_key
from src.core_engine.agents.banding_agent import PropertyBandingAgent
from src.core_engine.utils.fuzzy_match import fuzzy_match_hard_config
from src.core_engine.utils.geo import calculate_distance_km
from src.core_engine.utils.iqr_analysis import calculate_iqr_rent_range
from src.models.property import Property


class PropertyBandingState(TypedDict):
    new_property: Property
    all_properties: list[Property]
    radius_km: float
    area_tolerance_percent: float
    filtered_properties: list[Property] | None
    banding_result: dict[str, Any] | None
    iqr_analysis: dict[str, float] | None


def filter_similar_properties(state: PropertyBandingState) -> dict[str, list[Property]]:
    new_prop = state["new_property"]
    all_props = state["all_properties"]
    radius_km = state["radius_km"]
    area_tolerance = state["area_tolerance_percent"]

    filtered = []

    for prop in all_props:
        if prop.id == new_prop.id:
            continue

        if not fuzzy_match_hard_config(new_prop.hard_config, prop.hard_config, area_tolerance):
            continue

        distance = calculate_distance_km(
            new_prop.latitude, new_prop.longitude, prop.latitude, prop.longitude
        )

        if distance <= radius_km:
            filtered.append(prop)

    return {"filtered_properties": filtered}


def band_properties(state: PropertyBandingState) -> dict[str, Any]:
    filtered_props = state["filtered_properties"]

    if not filtered_props:
        return {"banding_result": None}

    agent = PropertyBandingAgent(anthropic_api_key=get_anthropic_api_key())

    result = agent.band_properties(state["new_property"], filtered_props)

    return {
        "banding_result": {
            "bands": result.bands,
            "parameters_used": result.parameters_used,
            "parameters_rationale": result.parameters_rationale,
            "new_property_band": result.new_property_band,
            "confidence_score": result.confidence_score,
        }
    }


def calculate_band_iqr(state: PropertyBandingState) -> dict[str, Any]:
    banding_result = state["banding_result"]

    if not banding_result:
        return {"iqr_analysis": None}

    new_property_band = banding_result["new_property_band"]
    band_property_ids = banding_result["bands"].get(new_property_band, [])

    filtered_props = state["filtered_properties"]
    if filtered_props is None:
        return {"iqr_analysis": None}

    band_properties = [p for p in filtered_props if p.id in band_property_ids]

    rents = [p.current_rent for p in band_properties if p.current_rent is not None]

    if not rents:
        return {"iqr_analysis": None}

    iqr_result = calculate_iqr_rent_range(rents)

    return {"iqr_analysis": iqr_result}


def create_property_banding_graph() -> CompiledStateGraph:
    workflow = StateGraph(PropertyBandingState)

    workflow.add_node("filter_properties", filter_similar_properties)
    workflow.add_node("band_properties", band_properties)
    workflow.add_node("calculate_iqr", calculate_band_iqr)

    workflow.add_edge("filter_properties", "band_properties")
    workflow.add_edge("band_properties", "calculate_iqr")
    workflow.add_edge("calculate_iqr", END)

    workflow.set_entry_point("filter_properties")

    return workflow.compile()


def analyze_property_with_banding(
    new_property: Property,
    all_properties: list[Property],
    radius_km: float = 2.0,
    area_tolerance_percent: float = 15.0,
) -> dict[str, Any]:
    workflow = create_property_banding_graph()

    initial_state = {
        "new_property": new_property,
        "all_properties": all_properties,
        "radius_km": radius_km,
        "area_tolerance_percent": area_tolerance_percent,
        "filtered_properties": None,
        "banding_result": None,
        "iqr_analysis": None,
    }

    final_state = workflow.invoke(initial_state)

    return {
        "filtered_properties": final_state["filtered_properties"],
        "banding_result": final_state["banding_result"],
        "iqr_analysis": final_state["iqr_analysis"],
    }
