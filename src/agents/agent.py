import logging

from langgraph.graph import END, START, MessagesState, StateGraph

from .nodes import chat_node

logger = logging.getLogger("easeai")


builder = StateGraph(MessagesState)
builder.add_node("chat", chat_node)
builder.add_edge(START, "chat")
builder.add_edge("chat", END)
agent = builder.compile()
