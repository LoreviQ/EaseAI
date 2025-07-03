import logging

from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool

from ..state import OverallState

logger = logging.getLogger("easeai")

tools: list[BaseTool] = []
tools_by_name = {tool.name: tool for tool in tools}


def call_tool(state: OverallState, config: RunnableConfig) -> OverallState:
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
    return {"messages": outputs}
