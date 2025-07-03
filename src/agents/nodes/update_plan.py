import logging

from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig

from src.types import PresentationPlan

from ..state import OverallState

logger = logging.getLogger("easeai")


def update_plan(state: OverallState, config: RunnableConfig) -> OverallState:
    # Get the plan patch from the tool call
    for tool_call in state["messages"][-1].tool_calls:
        if tool_call.name == "update_plan":
            plan_patch = tool_call.args

    # Update the plan
    current_plan = state.get("presentation_plan") or PresentationPlan()
    updated_plan = PresentationPlan(
        title=plan_patch.get("title", current_plan.title),
        objective=plan_patch.get("objective", current_plan.objective),
        target_audience=plan_patch.get("target_audience", current_plan.target_audience),
        tone=plan_patch.get("tone", current_plan.tone),
        duration=plan_patch.get("duration", current_plan.duration),
        research_summary=plan_patch.get(
            "research_summary", current_plan.research_summary
        ),
    )

    # Create a tool message
    message = ToolMessage(
        content="Plan updated successfully",
        name="update_plan",
    )

    return {
        "messages": [message],
        "presentation_plan": updated_plan,
    }
