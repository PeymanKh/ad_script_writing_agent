# Import libraries
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import get_usage_metadata_callback

from src.config.config import config
from src.config.logging_config import get_logger
from src.agent.state import AgentState, VideoScriptDraft, StaticAdDraft, VariationRequest
from src.agent.utils import build_variation_generation_message

logger = get_logger(__name__)


def variation_generation_node(state: AgentState) -> AgentState:
    """
    Generates a single A/B test variant with hook, CTA, and emotional tone changes.
    This variant will then go through evaluation and refinement.
    """
    logger.info("--- Entering Single Variation Generation Node ---")

    if not state.script_draft:
        logger.error("No script_draft found for variation generation.")
        raise ValueError("Approved script draft is missing for variation generation.")

    try:
        llm = ChatOpenAI(
            model=config.script_generation_llm1,
            api_key=config.script_generation_api_key1,
            temperature=config.script_generation_temperature1
        )

        # Determine output schema based on platform
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

        structured_llm = llm.with_structured_output(output_schema, method='json_mode')
        messages_list = build_variation_generation_message(state)

        # Track token usage
        with get_usage_metadata_callback() as cb:
            response = structured_llm.invoke(messages_list)

        # Extract token usage
        token_usage = cb.usage_metadata
        total_tokens = sum(usage.get('total_tokens', 0) for usage in token_usage.values())

        # Create variation request details
        variation_request = VariationRequest(
            variation_focus="Hook + CTA + Emotional Tone Enhancement",
            target_changes=[
                "Modified opening hook using different audience pain point/aspiration",
                "Enhanced call-to-action with stronger urgency and emotional resonance",
                "Shifted emotional tone to align with different audience values/preferences"
            ]
        )

        logger.info(f"Generated single variation script for A/B testing")

        # Update AgentState with the variation draft (ready for evaluation)
        return state.model_copy(update={
            "variation_request": variation_request,
            "variation_script_draft": response,
            "is_variation_workflow": True,
            "total_llm_tokens": state.total_llm_tokens + total_tokens,
        })

    except Exception as e:
        logger.error(f"Error in Single Variation Generation Node: {e}", exc_info=True)
        raise
