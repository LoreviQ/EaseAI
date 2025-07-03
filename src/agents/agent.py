import logging

from langgraph.graph import END, START, StateGraph

from src.types import ProjectPhase

from .nodes import planner, update_plan
from .state import OverallState

logger = logging.getLogger("easeai")


def phase_router(state: OverallState) -> str:
    if state["project_phase"] == ProjectPhase.PREPARATION:
        return "planner"
    return END


def response_router(state: OverallState) -> str:
    if state["messages"][-1].tool_calls:
        return "update_plan"
    return END


builder = StateGraph(OverallState)
builder.add_conditional_edges(START, phase_router)

# Planning phase
builder.add_node("planner", planner)
builder.add_node("update_plan", update_plan)
builder.add_conditional_edges("planner", response_router)
builder.add_edge("update_plan", "planner")


agent = builder.compile()
