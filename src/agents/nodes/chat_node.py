import logging

from ..state import InputState, OutputState

logger = logging.getLogger("easeai")


def chat_node(state: InputState) -> OutputState:
    return {"agent_response": f"Response to: {state['user_input']}"}
