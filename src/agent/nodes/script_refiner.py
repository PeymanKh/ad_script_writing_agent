# Import libraries
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import get_usage_metadata_callback

from src.config.config import config
from src.agent.state import AgentState, VideoScriptDraft, StaticAdDraft
from src.config.logging_config import get_logger
from src.agent.utils import build_script_refinement_message

logger = get_logger(__name__)


def script_refinement_node(state: AgentState) -> AgentState:
    """
    Refines the ad script based on the evaluation report's actionable recommendations.
    """
    logger.info("Start Script Refinement Node...")

    # Ensure necessary data is present for refinement
    if not state.script_draft:
        logger.error("No script_draft found for refinement.")
        raise ValueError("Script draft is missing for refinement.")
    if not state.evaluation_report:
        logger.error("No evaluation_report found for refinement. Cannot refine without feedback.")
        raise ValueError("Evaluation report is missing for script refinement.")

    # Define video and static platforms for a clean conditional check
    video_platforms = [
        "instagram_reels", "instagram_stories", "facebook_stories",
        "youtube_shorts", "tiktok_feed", "snapchat_spotlight"
    ]
    static_platforms = [
        "instagram_feeds", "facebook_feeds"
    ]

    # Select the correct schema based on the ad platform
    if state.ad_platform.value in video_platforms:
        output_schema = VideoScriptDraft
    elif state.ad_platform.value in static_platforms:
        output_schema = StaticAdDraft
    else:
        # Handle unsupported platforms gracefully
        raise ValueError(f"Ad platform {state.ad_platform.value} is not supported by the script refiner.")

    try:
        llm = ChatOpenAI(
            model=config.script_evaluation_and_refinement_llm,
            api_key=config.script_evaluation_and_refinement_api_key,
            temperature=config.script_evaluation_and_refinement_temperature
        )

        # The refinement node will output a new (refined) ScriptDraft
        structured_llm = llm.with_structured_output(output_schema, method='json_mode')

        # Build the messages list, passing relevant state data
        messages_list = build_script_refinement_message(state)

        logger.info("Calling LLM for script refinement...")

        with get_usage_metadata_callback() as cb:
            response: output_schema = structured_llm.invoke(messages_list)

        iteration_log = state.script_iteration_history or []

        iteration_log.append({
            "timestamp": datetime.now().isoformat(),
            "action": "script_refined",
            "previous_evaluation_report": state.evaluation_report.model_dump(),
            "output_refined_script": response.model_dump(),
        })

        # Extract token usage from the callback
        token_usage = cb.usage_metadata
        total_tokens = 0

        for model_name, usage in token_usage.items():
            total_tokens += usage.get('total_tokens', 0)


        # Update AgentState with the refined script
        return state.model_copy(update={
            "script_draft": response,
            "script_iteration_history": iteration_log,
            "revision_feedback": None,
            "iteration_count": state.iteration_count + 1,
            "total_llm_tokens": state.total_llm_tokens + total_tokens,
        })

    except Exception as e:
        logger.error(f"Error in ScriptRefinementNode: {e}", exc_info=True)
        raise