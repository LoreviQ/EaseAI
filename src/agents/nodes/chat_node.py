import logging

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig

from src.database import MessagesAdapter
from src.types import ProjectPhase

from ..state import OverallState

logger = logging.getLogger("easeai")


def chat_node(state: OverallState, config: RunnableConfig) -> OverallState:
    user_message = state["messages"][-1].content
    response = "Response to: " + user_message

    # Save the response to the database
    project_id = config["configurable"]["project_id"]
    db_session = config["configurable"]["db_session"]
    MessagesAdapter(db_session).create_message(
        project_id=project_id,
        role="ai",
        content=response,
    )
    if user_message == "ADVANCE PHASE":
        return {
            "messages": [AIMessage(content=response)],
            "project_phase": ProjectPhase.GENERATION,
        }
    return {"messages": [AIMessage(content=response)]}
