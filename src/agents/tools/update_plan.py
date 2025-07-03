import logging
from typing import Optional

from langchain_core.tools import tool

from src.types import PresentationPlan

from ..state import get_state, make_change

logger = logging.getLogger("easeai")


@tool("update_plan", args_schema=PresentationPlan)
def update_plan_tool(
    title: Optional[str] = None,
    objective: Optional[str] = None,
    target_audience: Optional[str] = None,
    tone: Optional[str] = None,
    duration: Optional[str] = None,
    research_summary: Optional[str] = None,
) -> str:
    """Empty tool for schema"""
    state = get_state()
    if state is None:
        raise ValueError("No state found")
    current_plan = state.get("presentation_plan") or PresentationPlan()
    updated_plan = PresentationPlan(
        title=title or current_plan.title,
        objective=objective or current_plan.objective,
        target_audience=target_audience or current_plan.target_audience,
        tone=tone or current_plan.tone,
        duration=duration or current_plan.duration,
        research_summary=research_summary or current_plan.research_summary,
    )
    make_change("presentation_plan", updated_plan)
    return "Plan updated"
