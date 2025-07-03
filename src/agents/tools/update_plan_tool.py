import logging
from typing import Optional

from langchain_core.tools import tool

from src.types import PresentationPlan

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
    pass
