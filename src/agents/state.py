from typing import Dict, Optional

from langgraph.graph import MessagesState
from typing_extensions import Annotated

from src.types import PresentationPlan, ProjectPhase, Slide, update_plan, update_slides


class InputState(MessagesState):
    project_phase: ProjectPhase
    presentation_plan: Annotated[Optional[PresentationPlan], update_plan]


class OverallState(MessagesState):
    project_phase: ProjectPhase
    presentation_plan: Annotated[Optional[PresentationPlan], update_plan]
    slides: Annotated[Optional[Dict[int, Slide]], update_slides]
