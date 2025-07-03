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


class SlideContent(BaseModel):
    slide_number: int
    content: str


class SlideContentResponse(BaseModel):
    slides: List[SlideContent]


# llm
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    max_retries=2,
)
structured_llm = llm.with_structured_output(SlideContentResponse)

# prompts
slide_generator_prompt = PromptTemplate(
    template="""You are EaseAI, an AI assistant helping users create presentations.
Your goal is to generate compelling slide content for each slide in the presentation.

# Current Presentation Plan:
{current_plan}

# Slide Outlines:
{slide_outlines}

Create engaging, visually appealing slides that effectively communicate your message.
Focus on:
- Clear, concise messaging that serves the presentation's purpose
- Visual hierarchy and readability
- Professional design that matches the intended tone
- Content that resonates with the target audience
- Strategic use of bullet points, headings, and white space
- Appropriate balance of text and visual elements

For each slide, generate HTML/CSS/JS content that can be embedded in a web component.
The content should be self-contained and responsive.
Use modern web technologies and best practices.
Make the design clean, professional, and engaging.""",
    input_variables=[
        "current_plan",
        "slide_outlines",
    ],
)
step_instructions = (
    "Generate the complete slide content as HTML/CSS/JS for each slide outline. "
    "Each slide's content should be production-ready and visually appealing. "
    "Focus on creating slides that will captivate the audience and effectively deliver the intended message. "  # noqa: E501
    "Return a list of SlideContent objects with slide numbers and content strings."
)


# node
def slide(state: OverallState, config: RunnableConfig) -> OverallState:
    slides = state.get("slides", {})
    slide_outlines = "\n".join(str(slide) for slide in slides.values())
    system = slide_generator_prompt.format(
        current_plan=state.get("presentation_plan"),
        slide_outlines=slide_outlines,
    )
    logger.debug(f"System prompt: {system}")
    messages = (
        [SystemMessage(content=system)]
        + state.get("messages", [])
        + [SystemMessage(content=step_instructions)]
    )
    response: SlideContentResponse = structured_llm.invoke(messages, config)

    # Create dictionary of slide content updates
    slide_updates: Dict[int, Slide] = {}
    for slide_content in response.slides:
        slide_updates[slide_content.slide_number] = Slide(content=slide_content.content)

    return {
        "slides": slide_updates,
    }
