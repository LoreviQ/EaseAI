from typing import TypedDict


class OverallState(TypedDict):
    user_input: str
    agent_response: str


class InputState(TypedDict):
    user_input: str


class OutputState(TypedDict):
    agent_response: str
