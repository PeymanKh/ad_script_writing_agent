# Import libraries
from langchain_openai import ChatOpenAI

from src.config.config import config
from src.config.logging_config import get_logger
from src.agent.state import AgentState, FinalScriptVariants
from src.agent.utils import build_variation_generation_message

logger = get_logger(__name__)


def variation_generation_node(state: AgentState) -> AgentState:
    """
    Generates multiple A/B test variants of the approved ad script.
    """
    logger.info("--- Entering VariationGenerationNode ---")

    if not state.script_draft:
        logger.error("No script_draft found for variation generation.")
        raise ValueError("Approved script draft is missing for variation generation.")

    def call_llm_with_retries(messages):
        llm = ChatOpenAI(
            model="gpt-4o",
            api_key=config.openai_api_key,
            temperature=0.7
        )
        structured_llm = llm.with_structured_output(FinalScriptVariants, method='json_mode')
        return structured_llm.invoke(messages)

    try:
        messages_list = build_variation_generation_message(state)

        response: FinalScriptVariants = call_llm_with_retries(messages_list)

        # Update AgentState with the generated variants
        return state.model_copy(update={
            "final_scripts_variants": response,
        })

    except Exception as e:
        logger.error(f"Error in VariationGenerationNode: {e}", exc_info=True)
        raise
