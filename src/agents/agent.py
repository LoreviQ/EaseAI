import logging

from langgraph.graph import END, START, StateGraph

from .nodes import chat_node
from .state import InputState, OutputState, OverallState

logger = logging.getLogger("easeai")


builder = StateGraph(OverallState, input_schema=InputState, output_schema=OutputState)
builder.add_node("chat", chat_node)
builder.add_edge(START, "chat")
builder.add_edge("chat", END)
agent = builder.compile()
