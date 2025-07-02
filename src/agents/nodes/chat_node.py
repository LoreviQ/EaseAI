import logging

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import MessagesState

from src.database import MessagesAdapter

logger = logging.getLogger("easeai")


def chat_node(state: MessagesState, config: RunnableConfig) -> MessagesState:
    response = "Response to: " + state["messages"][-1].content

    # Save the response to the database
    project_id = config["configurable"]["project_id"]
    db_session = config["configurable"]["db_session"]
    MessagesAdapter(db_session).create_message(
        project_id=project_id,
        role="ai",
        content=response,
    )
    return {"messages": [AIMessage(content=response)]}
