import logging
from typing import Optional

from langchain_core.messages import SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

from src.types import PresentationPlan

from ..state import OverallState

logger = logging.getLogger("easeai")
gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    max_retries=2,
)
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


class PlannerResponse(BaseModel):
    response: str = Field(description="The response from to the user")
    presentation_plan: Optional[PresentationPlan] = Field(
        description="The presentation plan patch. Only include changes you wish to make to the current plan"  # noqa: E501
    )


structured_planner = gemini_llm.with_structured_output(PlannerResponse)


def planner(state: OverallState, config: RunnableConfig) -> OverallState:
    system = planner_prompt.format(
        current_plan=state.get("presentation_plan"),
    )
    logger.debug(f"System prompt: {system}")
    messages = [SystemMessage(content=system)] + state.get("messages", [])
    response = structured_planner.invoke(messages, config)
    return {
        "messages": [response.response],
        "presentation_plan": response.presentation_plan,
    }
