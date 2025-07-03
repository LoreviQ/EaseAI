import logging
from typing import Dict, List

from langchain_core.messages import SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

from src.types import Slide

from ..state import OverallState

logger = logging.getLogger("easeai")


class DeliveryTutorialContent(BaseModel):
    slide_number: int
    delivery_tutorial: str


class DeliveryTutorialResponse(BaseModel):
    slides: List[DeliveryTutorialContent]


# llm
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    max_retries=2,
)
structured_llm = llm.with_structured_output(DeliveryTutorialResponse)

# prompts
delivery_tutorial_prompt = PromptTemplate(
    template="""You are EaseAI, an AI assistant helping users create presentations.
Your goal is to generate delivery tutorials for each slide in the presentation.

# Current Presentation Plan:
{current_plan}

# Current Slides:
{current_slides}

Create detailed delivery tutorials that will help the presenter deliver each slide with confidence and impact.
Focus on:
- Voice tone and pacing recommendations
- Body language and gesture suggestions
- Eye contact and audience engagement techniques
- Emphasis points and dramatic pauses
- Visual cues and slide interaction guidance
- Timing recommendations for each section
- Energy level and enthusiasm markers
- Potential stumbling blocks and how to recover
- Techniques for maintaining audience attention

The delivery tutorials should be practical, actionable advice that transforms good content into compelling presentations.
They should help presenters connect with their audience and deliver memorable experiences.""",  # noqa: E501
    input_variables=[
        "current_plan",
        "current_slides",
    ],
)
step_instructions = (
    "Generate comprehensive delivery tutorials for each slide. "
    "The tutorials should provide specific guidance on how to present each slide effectively. "  # noqa: E501
    "Focus on creating actionable advice that will help the presenter deliver with confidence and impact. "  # noqa: E501
    "Return a list of DeliveryTutorialContent objects with slide numbers and delivery tutorials."  # noqa: E501
)


# node
def delivery_tutorial(state: OverallState, config: RunnableConfig) -> OverallState:
    slides = state.get("slides", {})
    current_slides = "\n".join(str(slide) for slide in slides.values())
    system = delivery_tutorial_prompt.format(
        current_plan=state.get("presentation_plan"),
        current_slides=current_slides,
    )
    logger.debug(f"System prompt: {system}")
    messages = (
        [SystemMessage(content=system)]
        + state.get("messages", [])
        + [SystemMessage(content=step_instructions)]
    )
    response: DeliveryTutorialResponse = structured_llm.invoke(messages, config)

    # Create dictionary of delivery tutorial updates
    tutorial_updates: Dict[int, Slide] = {}
    for tutorial_content in response.slides:
        tutorial_updates[tutorial_content.slide_number] = Slide(
            delivery_tutorial=tutorial_content.delivery_tutorial
        )

    return {
        "slides": tutorial_updates,
    }
