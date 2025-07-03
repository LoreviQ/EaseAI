import logging

from langgraph.graph import END, START, StateGraph

from src.types import ProjectPhase

from .nodes import call_tool, planner
from .state import OverallState

logger = logging.getLogger("easeai")


def phase_router(state: OverallState) -> str:
    if state["project_phase"] == ProjectPhase.PREPARATION:
        return "planner"
    return END


def response_router(state: OverallState) -> str:
    if state["messages"][-1].tool_calls:
        return "call_tool"
    return END


builder = StateGraph(OverallState)
builder.add_conditional_edges(START, phase_router)

# Planning phase
builder.add_node("planner", planner)
builder.add_node("call_tool", call_tool)
builder.add_conditional_edges("planner", response_router)
builder.add_edge("call_tool", "planner")


agent = builder.compile()
