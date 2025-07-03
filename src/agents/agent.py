import logging

from langgraph.graph import END, START, StateGraph

from src.types import ProjectPhase

from .nodes import (
    call_tool,
    delivery_tutorial_generator,
    outline,
    planner,
    slide_generator,
    speaker_notes_generator,
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
builder.add_node("slide_generator", slide_generator)
builder.add_node("speaker_notes_generator", speaker_notes_generator)
builder.add_node("delivery_tutorial_generator", delivery_tutorial_generator)
builder.add_edge("outline", "slide_generator")
builder.add_edge("slide_generator", "speaker_notes_generator")
builder.add_edge("speaker_notes_generator", "delivery_tutorial_generator")
builder.add_edge("delivery_tutorial_generator", END)

agent = builder.compile()
