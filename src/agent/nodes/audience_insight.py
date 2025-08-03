# Import libraries
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.callbacks import get_usage_metadata_callback

from src.config.config import config
from src.config.logging_config import get_logger
from src.agent.utils import build_audience_insight_message
from src.agent.state import AgentState, AudienceInsight


logger = get_logger(__name__)


def audience_insight_node(state: AgentState) -> AgentState:
    try:
        logger.info("Start Audience Insight Node")
        llm = ChatGoogleGenerativeAI(
            model=config.audience_insight_llm,
            api_key=config.audience_insight_api_key,
            temperature=config.audience_insight_temperature
        )

        structured_llm = llm.with_structured_output(AudienceInsight, method='json_mode')

        messages_list = build_audience_insight_message(state)

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
            "audience_insight": response,
            "total_llm_tokens": state.total_llm_tokens + total_tokens,
        })

    except Exception as e:
        logger.error(f"LLM invocation failed: {e}", exc_info=True)
        raise
