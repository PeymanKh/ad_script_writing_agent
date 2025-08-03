# Import libraries
from typing import List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import get_usage_metadata_callback

from src.agent.state import AgentState
from src.config.config import config
from src.config.logging_config import get_logger
from src.agent.utils import build_creative_strategy_message


logger = get_logger(__name__)


class CreativeStrategyResponse(BaseModel):
    """Node's response schema"""
    core_message_pillars: List[str] = Field(
        description="3 most important messages the ad should convey."
    )
    brainstormed_hooks: List[str] = Field(
        description="3-5 ideas for attention-grabbing opening lines."
    )
    generated_ctas: List[str] = Field(
        description="A set of diverse Call-to-Action phrases relevant to the campaign_goal and brand_voice."
    )
    emotional_triggers: List[str] = Field(
        description="Specific emotions to evoke in the audience."
    )
    primary_visual_concept: str = Field(
        description="A brief description of the recommended visual style and concepts for the ad."
    )
    audio_strategy: str = Field(
        description="A brief description of the recommended audio strategy (e.g., trending music, voiceover)."
    )


def creative_strategy_node(state: AgentState) -> AgentState:
    try:
        logger.info("Start Creative Strategy Node")
        llm = ChatOpenAI(
            model=config.creative_strategy_llm,
            api_key=config.creative_strategy_api_key,
            temperature=config.creative_strategy_temperature
        )

        structured_llm = llm.with_structured_output(CreativeStrategyResponse, method='json_mode')

        messages_list = build_creative_strategy_message(state)

        # Call model and parse structured response
        with get_usage_metadata_callback() as cb:
            response = structured_llm.invoke(messages_list)

        logger.info("End Creative Strategy Node")

        # Extract token usage from the callback
        token_usage = cb.usage_metadata
        total_tokens = 0

        for model_name, usage in token_usage.items():
            total_tokens += usage.get('total_tokens', 0)

        # Unpack results and return a new AgentState with fields populated
        return state.model_copy(update={
            "core_message_pillars": response.core_message_pillars,
            "brainstormed_hooks": response.brainstormed_hooks,
            "generated_ctas": response.generated_ctas,
            "emotional_triggers": response.emotional_triggers,
            "primary_visual_concept": response.primary_visual_concept,
            "audio_strategy": response.audio_strategy,
            "total_llm_tokens": state.total_llm_tokens + total_tokens,
        })

    except Exception as e:
        logger.error(f"LLM invocation failed: {e}", exc_info=True)
        raise
