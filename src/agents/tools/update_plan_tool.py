import logging
from typing import Optional

from langchain_core.tools import tool

from src.types import PresentationPlan

logger = logging.getLogger("easeai")


def create_update_plan_tool(plan_container: dict):
    @tool("update_plan", args_schema=PresentationPlan)
    def update_plan_tool(
        title: Optional[str] = None,
        objective: Optional[str] = None,
        target_audience: Optional[str] = None,
        tone: Optional[str] = None,
        duration: Optional[str] = None,
        research_summary: Optional[str] = None,
    ) -> str:
        """Sets or updates the presentation plan with the provided details."""
        try:
            current_plan = plan_container.get("plan") or PresentationPlan()
            updated_plan = PresentationPlan(
                title=title or current_plan.title,
                objective=objective or current_plan.objective,
                target_audience=target_audience or current_plan.target_audience,
                tone=tone or current_plan.tone,
                duration=duration or current_plan.duration,
                research_summary=research_summary or current_plan.research_summary,
            )
            plan_container["plan"] = updated_plan
            return f"Presentation plan updated successfully: {updated_plan.title}"
        except Exception as e:
            logger.error(f"Error updating plan: {e}")
            return f"Error updating plan: {str(e)}"

    return update_plan_tool
