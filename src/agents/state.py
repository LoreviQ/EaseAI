from langgraph.graph import MessagesState

from src.types import ProjectPhase


class OverallState(MessagesState):
    project_phase: ProjectPhase
