from typing import Optional

from langgraph.graph import MessagesState

from src.types import PresentationPlan, ProjectPhase


class OverallState(MessagesState):
    project_phase: ProjectPhase
    presentation_plan: Optional[PresentationPlan] = None
