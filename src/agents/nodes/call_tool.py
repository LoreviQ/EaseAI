import logging

from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig

from ..state import OverallState, get_changes, state_context
from .planner import tools as planner_tools

logger = logging.getLogger("easeai")
tools_by_name = {tool.name: tool for tool in planner_tools}


def call_tool(state: OverallState, config: RunnableConfig) -> OverallState:
    # Get the plan patch from the tool call
    with state_context(state):
        outputs = []
        for tool_call in state["messages"][-1].tool_calls:
            tool_result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
            outputs.append(
                ToolMessage(
                    content=tool_result,
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        # Update the state
        changes = get_changes()
        changes["messages"] = outputs
        return changes
