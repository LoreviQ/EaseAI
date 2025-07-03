import logging
from typing import List

from langchain_core.messages import SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool
from langchain_google_genai import ChatGoogleGenerativeAI

from ..state import OverallState
from ..tools import update_plan_tool

logger = logging.getLogger("easeai")
gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    max_retries=2,
)
tools: List[BaseTool] = [update_plan_tool]
planner_model = gemini_llm.bind_tools(tools)
planner_prompt = PromptTemplate(
    template="""You are EaseAI, an AI assistant helping users create presentations.

        Your goal is to help users build and refine their presentation plan through conversation.
        Ask the user questions about their desired presentation to help build the presentation plan.
        Use the update_plan tool to create or update the presentation plan based on user input.

        # Current Presentation Plan:
        {current_plan}""",  # noqa: E501
    input_variables=[
        "current_plan",
    ],
)


def planner(state: OverallState, config: RunnableConfig) -> OverallState:
    system = planner_prompt.format(
        current_plan=state.get("presentation_plan"),
    )
    logger.debug(f"System prompt: {system}")
    messages = [SystemMessage(content=system)] + state.get("messages", [])
    response = planner_model.invoke(messages, config)
    return {
        "messages": [response],
    }
