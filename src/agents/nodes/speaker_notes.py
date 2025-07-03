import logging
from typing import Dict, List

from langchain_core.messages import SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

from src.types import Slide

from ..state import InputState, OverallState

logger = logging.getLogger("easeai")


class SpeakerNotesContent(BaseModel):
    slide_number: int
    speaker_notes: str


class SpeakerNotesResponse(BaseModel):
    slides: List[SpeakerNotesContent]


# llm
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    max_retries=2,
)
structured_llm = llm.with_structured_output(SpeakerNotesResponse)

# prompts
speaker_notes_prompt = PromptTemplate(
    template="""You are EaseAI, an AI assistant helping users create presentations.
Your goal is to generate comprehensive speaker notes for each slide in the presentation.

# Current Presentation Plan:
{current_plan}

# Current Slides:
{current_slides}

Create detailed speaker notes that will help the presenter deliver an engaging and informative presentation.
Focus on:
- Key talking points that expand on the slide content
- Smooth transitions between slides
- Engaging storytelling and examples
- Audience interaction opportunities
- Timing and pacing guidance
- Important facts, statistics, or quotes to mention
- Potential questions from the audience and how to address them

The speaker notes should be conversational and natural, helping the presenter sound confident and knowledgeable.
They should complement the slide content without simply repeating it.""",  # noqa: E501
    input_variables=[
        "current_plan",
        "current_slides",
    ],
)
step_instructions = (
    "Generate comprehensive speaker notes for each slide. "
    "The notes should provide detailed guidance for what to say and how to present each slide effectively. "  # noqa: E501
    "Focus on creating notes that will help the presenter deliver a compelling and professional presentation. "  # noqa: E501
    "Return a list of SpeakerNotesContent objects with slide numbers and speaker notes."
)


# node
def speaker_notes(state: InputState, config: RunnableConfig) -> OverallState:
    slides = state.get("slides", {})
    current_slides = "\n".join(str(slide) for slide in slides.values())
    system = speaker_notes_prompt.format(
        current_plan=state.get("presentation_plan"),
        current_slides=current_slides,
    )
    logger.debug(f"System prompt: {system}")
    messages = (
        [SystemMessage(content=system)]
        + state.get("messages", [])
        + [SystemMessage(content=step_instructions)]
    )
    response: SpeakerNotesResponse = structured_llm.invoke(messages, config)

    # Create dictionary of speaker notes updates
    notes_updates: Dict[int, Slide] = {}
    for notes_content in response.slides:
        notes_updates[notes_content.slide_number] = Slide(
            speaker_notes=notes_content.speaker_notes
        )

    return {
        "slides": notes_updates,
    }
