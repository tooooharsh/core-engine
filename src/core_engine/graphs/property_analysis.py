from typing import Any, TypedDict

from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.core_engine.agents.property_agents import PriceAnalyzerTool, PropertyFilterTool
from src.models.property import PropertyListing


class PropertyAnalysisState(TypedDict):
    properties: list[PropertyListing]
    reference_property: PropertyListing
    radius_km: float
    filtered_properties: list[PropertyListing] | None
    price_analysis: dict[str, Any] | None


def create_property_analysis_graph() -> CompiledStateGraph:
    # Create tools
    property_filter = PropertyFilterTool()
    price_analyzer = PriceAnalyzerTool()

    # Create graph
    workflow = StateGraph(PropertyAnalysisState)

    # Define nodes
    workflow.add_node(
        "filter_properties",
        lambda state: {
            "filtered_properties": property_filter.run(
                {
                    "properties": state["properties"],
                    "reference_property": state["reference_property"],
                    "radius_km": state.get("radius_km", 2.0),
                }
            )
        },
    )

    workflow.add_node(
        "analyze_prices",
        lambda state: {
            "price_analysis": price_analyzer.run({"properties": state["filtered_properties"]})
        },
    )

    # Define edges
    workflow.add_edge("filter_properties", "analyze_prices")

    # End state
    workflow.set_entry_point("filter_properties")
    workflow.set_finish_point("analyze_prices")

    return workflow.compile()


def analyze_nearby_properties(
    properties: list[PropertyListing], reference_property: PropertyListing, radius_km: float = 2.0
) -> dict[str, Any]:
    """
    Analyze properties within a specified radius of a reference property.

    Args:
        properties: List of property listings to analyze
        reference_property: Reference property to calculate distance from
        radius_km: Radius in kilometers to filter properties (default: 2.0)

    Returns:
        Dictionary containing filtered properties and price analysis
    """
    workflow = create_property_analysis_graph()

    # Initialize state
    initial_state = {
        "properties": properties,
        "reference_property": reference_property,
        "radius_km": radius_km,
    }

    # Run workflow
    final_state = workflow.invoke(initial_state)

    return {
        "filtered_properties": final_state["filtered_properties"],
        "price_analysis": final_state["price_analysis"],
    }
