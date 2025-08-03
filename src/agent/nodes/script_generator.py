# Import libraries
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import get_usage_metadata_callback

from src.config.config import config
from src.agent.state import AgentState, VideoScriptDraft, StaticAdDraft, ScriptDraft
from src.config.logging_config import get_logger
from src.agent.utils import build_script_generation_message

logger = get_logger(__name__)


def script_generation_node(state: AgentState) -> AgentState:
    """
    Generates the ad script based on the campaign brief and creative strategy.
    """
    try:
        logger.info("Start Script Generation Node")
        llm = ChatOpenAI(
            model=config.script_generation_llm1,
            api_key=config.script_generation_api_key1,
            temperature=config.script_generation_temperature1
        )

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
            raise ValueError(f"Ad platform {state.ad_platform.value} is not supported by the script generator.")

        # Set up structured output for ScriptDraft
        structured_llm = llm.with_structured_output(output_schema, method='json_mode')

        # Build the messages list for the LLM call
        messages_list = build_script_generation_message(state)

        with get_usage_metadata_callback() as cb:
            response = structured_llm.invoke(messages_list)

        logger.info("End Script Generation Node")

        # Extract token usage from the callback
        token_usage = cb.usage_metadata
        total_tokens = 0

        for model_name, usage in token_usage.items():
            total_tokens += usage.get('total_tokens', 0)


        # Update AgentState with the generated script
        return state.model_copy(update={
            "script_draft": response,
            "total_llm_tokens": state.total_llm_tokens + total_tokens,
        })

    except Exception as e:
        raise
