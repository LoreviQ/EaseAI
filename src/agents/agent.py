import logging

from langgraph.graph import END, START, StateGraph

from src.types import ProjectPhase

from .nodes import (
    call_tool,
    delivery_tutorial,
    outline,
    planner,
    slide,
    speaker_notes,
)
from .state import OverallState

logger = logging.getLogger("easeai")


def phase_router(state: OverallState) -> str:
    phase = state["project_phase"]
    match phase:
        case ProjectPhase.PREPARATION:
            return "planner"
        case ProjectPhase.GENERATION:
            return "outline"
    return END


def response_router(state: OverallState) -> str:
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "call_tool"
    return END


builder = StateGraph(OverallState)
builder.add_conditional_edges(START, phase_router)

# Planning phase
builder.add_node("planner", planner)
builder.add_node("call_tool", call_tool)
builder.add_conditional_edges("planner", response_router)
builder.add_edge("call_tool", "planner")

# generation phase
builder.add_node("outline", outline)
builder.add_node("slide", slide)
builder.add_node("speaker_notes", speaker_notes)
builder.add_node("delivery_tutorial", delivery_tutorial)
builder.add_edge("outline", "slide")
builder.add_edge("slide", "speaker_notes")
builder.add_edge("speaker_notes", "delivery_tutorial")
builder.add_edge("delivery_tutorial", END)

agent = builder.compile()
