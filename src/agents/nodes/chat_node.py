import logging

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import MessagesState

logger = logging.getLogger("easeai")


def chat_node(state: MessagesState, config: RunnableConfig) -> MessagesState:
    response = "Response to: " + state["messages"][-1].content
    return {"messages": state["messages"] + [AIMessage(content=response)]}
