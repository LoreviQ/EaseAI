import logging
from typing import Any, Dict, Optional
from uuid import UUID

from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph
from sqlalchemy.orm import Session

from src.types import ProjectPhase

from .nodes import content_node, conversation_node, review_node
from .state import WorkflowState

logger = logging.getLogger("easeai")


class PresentationWorkflowAgent:
    """
    Main workflow agent for EaseAI presentation creation.

    Orchestrates the multi-stage presentation creation process:
    1. Conversation phase: Research and planning discussions
    2. Content generation: Slides, notes, and tutorial creation
    3. Review phase: Quality assurance and refinement
    """

    def __init__(self, session: Session):
        self.session = session
        self.graph = self._build_graph()

    def _build_graph(self) -> CompiledStateGraph:
        """Build the LangGraph workflow graph."""
        workflow = StateGraph(WorkflowState)

        # Add nodes
        workflow.add_node("conversation", self._conversation_wrapper)
        workflow.add_node("content_generation", self._content_wrapper)
        workflow.add_node("review", self._review_wrapper)

        # Define transitions based on project phase
        workflow.add_conditional_edges(
            "conversation",
            self._route_from_conversation,
            {
                "content_generation": "content_generation",
                "conversation": "conversation",
                "end": END,
            },
        )

        workflow.add_conditional_edges(
            "content_generation",
            self._route_from_content,
            {"review": "review", "end": END},
        )

        workflow.add_conditional_edges(
            "review",
            self._route_from_review,
            {
                "conversation": "conversation",
                "content_generation": "content_generation",
                "end": END,
            },
        )

        # Set entry point
        workflow.set_entry_point("conversation")

        return workflow.compile()

    def _conversation_wrapper(self, state: WorkflowState) -> WorkflowState:
        """Wrapper for conversation node with session injection."""
        return conversation_node(state, self.session)

    def _content_wrapper(self, state: WorkflowState) -> WorkflowState:
        """Wrapper for content node with session injection."""
        return content_node(state, self.session)

    def _review_wrapper(self, state: WorkflowState) -> WorkflowState:
        """Wrapper for review node with session injection."""
        return review_node(state, self.session)

    def _route_from_conversation(self, state: WorkflowState) -> str:
        """Determine next step from conversation phase."""
        current_phase = state.phase

        # For now, stay in conversation mode for all phases
        # TODO: Add logic to transition to content generation
        # when research and planning are complete
        return "conversation"

    def _route_from_content(self, state: WorkflowState) -> str:
        """Determine next step from content generation phase."""
        # TODO: Add logic to determine if content is ready for review
        return "review"

    def _route_from_review(self, state: WorkflowState) -> str:
        """Determine next step from review phase."""
        # TODO: Add logic to handle review outcomes
        # - Return to conversation for more input
        # - Return to content generation for revisions
        # - End if everything is approved
        return "end"

    def process_message(
        self,
        project_id: UUID,
        phase: ProjectPhase = ProjectPhase.PREPARATION,
        system_prompt: str = "You are a helpful AI assistant that helps users create presentations.",
        generation_config: Optional[Dict[str, Any]] = None,
    ) -> WorkflowState:
        """
        Process a user message and generate a response.

        Args:
            project_id: UUID of the project
            phase: Current project phase
            system_prompt: System prompt for the AI
            generation_config: Optional generation parameters for the model

        Returns:
            Updated workflow state with AI response
        """
        initial_state = WorkflowState(
            project_id=project_id,
            phase=phase,
            messages=[],
            system_prompt=system_prompt,
            context={},
            generation_config=generation_config if generation_config else {},
        )

        try:
            result = self.graph.invoke(initial_state)
            logger.info(f"Processed message for project {project_id}")
            return result  # type: ignore

        except Exception as e:
            logger.error(f"Error processing message for project {project_id}: {e}")
            raise
