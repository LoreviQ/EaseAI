import logging

from langchain_core.runnables import RunnableConfig

from src.database import SlidesAdapter

from ..state import OverallState

logger = logging.getLogger("easeai")


def write_results(state: OverallState, config: RunnableConfig) -> OverallState:
    """Write generated slides to database."""
    db_session = config["configurable"]["db_session"]
    project_id = config["configurable"]["project_id"]

    slides_data = state.get("slides", {})

    if not slides_data:
        logger.warning("No slides data found to write to database")
        return {}

    # Save each slide individually
    slides_adapter = SlidesAdapter(db_session)

    for slide_num, slide in slides_data.items():
        # Check if slide already exists for this project and slide number
        if slides_adapter.slide_exists(project_id, slide_num):
            slides_adapter.update_slide(project_id, slide_num, slide)
        else:
            slides_adapter.create_slide(project_id, slide)

    logger.info(
        f"Successfully wrote {len(slides_data)} slides to database "
        f"for project {project_id}"
    )
    return {}
