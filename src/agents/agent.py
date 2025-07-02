import logging

from langgraph.graph import END, START, StateGraph

from src.types import ProjectPhase

from .nodes import chat_node
from .state import OverallState

logger = logging.getLogger("easeai")


def chat_conditional_edge(state: OverallState) -> str:
    if state["project_phase"] == ProjectPhase.PREPARATION:
        return "chat"
    return END


builder = StateGraph(OverallState)
builder.add_node("chat", chat_node)
builder.add_conditional_edges(START, chat_conditional_edge)
builder.add_edge("chat", END)
agent = builder.compile()
