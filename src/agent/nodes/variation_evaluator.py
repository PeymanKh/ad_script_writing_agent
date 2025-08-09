# Import libraries
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import get_usage_metadata_callback

from src.config.config import config
from src.agent.utils import build_evaluation_message
from src.config.logging_config import get_logger
from src.agent.state import AgentState, EvaluationReport

logger = get_logger(__name__)


def variation_evaluation_node(state: AgentState) -> AgentState:
    """
    Evaluates the generated variation script.
    """
    if not state.variation_script_draft:
        raise ValueError("Variation script draft is missing for evaluation.")

    try:
        logger.info("Start Variation Script Evaluation Node")

        llm = ChatOpenAI(
            model=config.script_evaluation_and_refinement_llm,
            api_key=config.script_evaluation_and_refinement_api_key,
            temperature=config.script_evaluation_and_refinement_temperature
        )

        structured_llm = llm.with_structured_output(EvaluationReport, method='json_mode')

        # Use variation script for evaluation by temporarily swapping
        temp_state = state.model_copy(update={"script_draft": state.variation_script_draft})
        messages_list = build_evaluation_message(temp_state)

        with get_usage_metadata_callback() as cb:
            response: EvaluationReport = structured_llm.invoke(messages_list)

        logger.info("End Variation Script Evaluation Node")

        # Extract token usage
        token_usage = cb.usage_metadata
        total_tokens = sum(usage.get('total_tokens', 0) for usage in token_usage.values())

        return state.model_copy(update={
            "variation_evaluation_report": response,
            "total_llm_tokens": state.total_llm_tokens + total_tokens,
        })

    except Exception as e:
        logger.error(f"Error in Variation Evaluation Node: {e}", exc_info=True)
        raise
