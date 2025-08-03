# Import libraries
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import get_usage_metadata_callback

from src.config.config import config
from src.agent.utils import build_evaluation_message
from src.config.logging_config import get_logger
from src.agent.state import AgentState, EvaluationReport


logger = get_logger(__name__)


def script_evaluation_node(state: AgentState) -> AgentState:
    """
    Evaluates the generated ad script and updates the AgentState with an EvaluationReport.
    """

    # Pre-check: Ensure script_draft exists before evaluation
    if not state.script_draft:
        raise ValueError("Script draft is missing for evaluation.")

    try:
        logger.info("Start Script Evaluation Node")

        llm = ChatOpenAI(
            model=config.script_evaluation_and_refinement_llm,
            api_key=config.script_evaluation_and_refinement_api_key,
            temperature=config.script_evaluation_and_refinement_temperature
        )

        # Set up structured output for EvaluationReport
        structured_llm = llm.with_structured_output(EvaluationReport, method='json_mode')

        # Build the messages list for the LLM call
        messages_list = build_evaluation_message(state)

        with get_usage_metadata_callback() as cb:
            response: EvaluationReport = structured_llm.invoke(messages_list)

        logger.info("End Script Evaluation Node")

        # Extract token usage from the callback
        token_usage = cb.usage_metadata
        total_tokens = 0

        for model_name, usage in token_usage.items():
            total_tokens += usage.get('total_tokens', 0)

        # Update AgentState with the evaluation report and revision feedback
        return state.model_copy(update={
            "evaluation_report": response,
            "revision_feedback": "\n".join(response.actionable_recommendations) if response.actionable_recommendations else None,
            "total_llm_tokens": state.total_llm_tokens + total_tokens,
        })

    except Exception as e:
        raise
