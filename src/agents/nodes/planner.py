import logging
from typing import Optional

from langchain_core.messages import SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

from src.database import MessagesAdapter, PresentationPlanAdapter
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
Take initiative to ask questions and provide guidance to the user.
Return the plan edits as a JSON object along with a response to the user.

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
    response: PlannerResponse = structured_planner.invoke(messages, config)

    # update database
    db_session = config["configurable"]["db_session"]
    project_id = config["configurable"]["project_id"]
    messages_adapter = MessagesAdapter(db_session)
    messages_adapter.create_message(
        project_id=project_id,
        role="ai",
        content=response.response,
    )
    if response.presentation_plan:
        presentation_plan_adapter = PresentationPlanAdapter(db_session)
        presentation_plan_adapter.update_plan(project_id, response.presentation_plan)
    return {
        "messages": [response.response],
        "presentation_plan": response.presentation_plan,
    }
