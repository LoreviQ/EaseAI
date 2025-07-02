import logging

from langgraph.graph import END, START, StateGraph

from src.types import ProjectPhase

from .nodes import planner_node
from .state import OverallState

logger = logging.getLogger("easeai")


def planner_conditional_edge(state: OverallState) -> str:
    if state["project_phase"] == ProjectPhase.PREPARATION:
        return "planner"
    return END


builder = StateGraph(OverallState)
builder.add_node("planner", planner_node)
builder.add_conditional_edges(START, planner_conditional_edge)
builder.add_edge("planner", END)
agent = builder.compile()
