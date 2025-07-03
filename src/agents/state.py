import threading
from contextlib import contextmanager
from typing import Any, Iterator, List, Optional

from langgraph.graph import MessagesState
from typing_extensions import Annotated

from src.types import PresentationPlan, ProjectPhase, Slide, update_plan

_thread_local = threading.local()


class InputState(MessagesState):
    project_phase: ProjectPhase
    presentation_plan: Annotated[Optional[PresentationPlan], update_plan]


class OverallState(MessagesState):
    project_phase: ProjectPhase
    presentation_plan: Annotated[Optional[PresentationPlan], update_plan]
    outlines: Optional[List[Slide]]


def get_state() -> Optional[OverallState]:
    return getattr(_thread_local, "state", None)


def get_changes() -> dict[str, Any]:
    return getattr(_thread_local, "state_changes", {})


def make_change(key: str, value: Any) -> None:
    _thread_local.state_changes[key] = value


@contextmanager
def state_context(state: OverallState) -> Iterator[None]:
    old_state = getattr(_thread_local, "state", None)
    _thread_local.state = state
    _thread_local.state_changes = {}
    try:
        yield
    finally:
        if old_state is None:
            delattr(_thread_local, "state")
        else:
            _thread_local.state = old_state
