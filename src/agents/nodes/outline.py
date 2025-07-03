import logging
from typing import List

from langchain_core.messages import SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

from src.types import Slide, SlideOutline

from ..state import InputState, OverallState

logger = logging.getLogger("easeai")


class OutlineResponse(BaseModel):
    slides: List[SlideOutline]


# llm
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    max_retries=2,
)
structured_llm = llm.with_structured_output(OutlineResponse)

# prompts
planner_prompt = PromptTemplate(
    template="""You are EaseAI, an AI assistant helping users create presentations.
Your goal is to help users build and refine their presentation plan through conversation.

# Current Presentation Plan:
{current_plan}""",  # noqa: E501
    input_variables=[
        "current_plan",
    ],
)
step_instructions = (
    "The current stage is to build a slide outline based on the presentation plan."
    "Think over what would make a compelling presentation and how to structure it."
    "Return the outline as a JSON object."
)


# node
def outline(state: InputState, config: RunnableConfig) -> OverallState:
    system = planner_prompt.format(
        current_plan=state.get("presentation_plan"),
    )
    logger.debug(f"System prompt: {system}")
    messages = (
        [SystemMessage(content=system)]
        + state.get("messages", [])
        + [SystemMessage(content=step_instructions)]
    )
    response: OutlineResponse = structured_llm.invoke(messages, config)

    # Convert outlines to Slide objects and create dictionary
    slides_dict = {}
    for outline in response.slides:
        slide = Slide(
            slide_number=outline.slide_number,
            title=outline.title,
            description=outline.description,
            time_spent_on_slide=outline.time_spent_on_slide,
        )
        slides_dict[outline.slide_number] = slide

    return {
        "slides": slides_dict,
    }
