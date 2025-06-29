import logging
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from sqlalchemy.orm import Session

from src.database import MessagesAdapter
from src.types import MessageRole

from ..state import WorkflowState

logger = logging.getLogger("easeai")


def conversation_node(state: WorkflowState, session: Session) -> WorkflowState:
    """
    Handle conversational interactions with the user.

    This node processes user messages and generates AI responses using Gemini 2.5 Flash.
    It maintains conversation history through the database and applies configurable
    system prompts based on the current project phase.

    Args:
        state: Current workflow state containing project context
        session: Database session for message persistence

    Returns:
        Updated state with new assistant message
    """
    messages_adapter = MessagesAdapter(session)

    # Get conversation history
    conversation_history, _ = messages_adapter.get_messages(project_id=state.project_id)

    # Initialize Gemini model
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")

    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.7,
        **(state.generation_config),
    )

    # Build message chain for Gemini
    messages = []

    # Add system prompt
    if state.system_prompt:
        messages.append(("system", state.system_prompt))

    # Add conversation history
    for msg in conversation_history:
        role = "user" if msg.role == MessageRole.USER else "ai"
        messages.append((role, msg.content))

    # Generate response
    try:
        response = model.invoke(messages)
        response_content = str(response.content)

        # Save assistant response to database
        assistant_message = messages_adapter.create_message(
            project_id=state.project_id,
            role=MessageRole.ASSISTANT.value,
            content=response_content,
        )

        # Update state with new message
        state.messages.append(assistant_message)

        logger.info(f"Generated response for project {state.project_id}")

        return state

    except Exception as e:
        logger.error(f"Error generating response: {e}")
        raise
