# Import libraries
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import get_usage_metadata_callback

from src.config.config import config
from src.agent.state import AgentState, VideoScriptDraft, StaticAdDraft
from src.config.logging_config import get_logger
from src.agent.utils import build_script_refinement_message

logger = get_logger(__name__)

def variation_refinement_node(state: AgentState) -> AgentState:
    """
    Refines the variation script based on evaluation feedback.
    """
    logger.info("Start Variation Script Refinement Node...")

    if not state.variation_script_draft:
        raise ValueError("Variation script draft is missing for refinement.")
    if not state.variation_evaluation_report:
        raise ValueError("Variation evaluation report is missing for refinement.")

    # Determine output schema
    video_platforms = [
        "instagram_reels", "instagram_stories", "facebook_stories",
        "youtube_shorts", "tiktok_feed", "snapchat_spotlight"
    ]
    static_platforms = [
        "instagram_feeds", "facebook_feeds"
    ]

    if state.ad_platform.value in video_platforms:
        output_schema = VideoScriptDraft
    elif state.ad_platform.value in static_platforms:
        output_schema = StaticAdDraft
    else:
        raise ValueError(f"Ad platform {state.ad_platform.value} is not supported.")

    try:
        llm = ChatOpenAI(
            model=config.script_evaluation_and_refinement_llm,
            api_key=config.script_evaluation_and_refinement_api_key,
            temperature=config.script_evaluation_and_refinement_temperature
        )

        structured_llm = llm.with_structured_output(output_schema, method='json_mode')

        # Use variation script and evaluation for refinement by temporarily swapping
        temp_state = state.model_copy(update={
            "script_draft": state.variation_script_draft,
            "evaluation_report": state.variation_evaluation_report
        })
        messages_list = build_script_refinement_message(temp_state)

        logger.info("Calling LLM for variation script refinement...")

        with get_usage_metadata_callback() as cb:
            response = structured_llm.invoke(messages_list)

        # Extract token usage
        token_usage = cb.usage_metadata
        total_tokens = sum(usage.get('total_tokens', 0) for usage in token_usage.values())

        # Update AgentState with the refined variation script
        return state.model_copy(update={
            "variation_script_draft": response,
            "variation_iteration_count": state.variation_iteration_count + 1,
            "total_llm_tokens": state.total_llm_tokens + total_tokens,
        })

    except Exception as e:
        logger.error(f"Error in Variation Refinement Node: {e}", exc_info=True)
        raise
