from langgraph.graph import StateGraph, START, END

from src.config.logging_config import get_logger
from src.agent.state import AgentState, SingleVariation

from src.agent.nodes.audience_insight import audience_insight_node
from src.agent.nodes.creative_strategy import creative_strategy_node
from src.agent.nodes.script_generator import script_generation_node
from src.agent.nodes.script_evaluator import script_evaluation_node
from src.agent.nodes.script_refiner import script_refinement_node
from src.agent.nodes.variation_generator import variation_generation_node
from src.agent.nodes.variation_evaluator import variation_evaluation_node
from src.agent.nodes.variation_refiner import variation_refinement_node

logger = get_logger(__name__)

MAX_REFINEMENT_ITERATIONS = 3
MAX_VARIATION_REFINEMENT_ITERATIONS = 3

def route_after_evaluation(state: AgentState) -> str:
    if state.evaluation_report and state.evaluation_report.is_approved_for_next_stage:
        logger.info("Script approved by AI. Moving to next node.")
        return END
    if state.iteration_count >= MAX_REFINEMENT_ITERATIONS:
        logger.warning(f"Max refinement iterations ({MAX_REFINEMENT_ITERATIONS}) reached. Ending workflow.")  # Fixed this line
        return END
    else:
        logger.info(f"Script not approved by AI. Iteration {state.iteration_count+1}/{MAX_REFINEMENT_ITERATIONS}. Sending to script_refinement_node for revision.")
        return "script_refinement_node"

# First graph (pre-review)
def build_pre_review_graph():
    builder = StateGraph(AgentState)
    builder.add_node("audience_insight_node", audience_insight_node)
    builder.add_node("creative_strategy_node", creative_strategy_node)
    builder.add_node("script_generation_node", script_generation_node)
    builder.add_node("script_evaluation_node", script_evaluation_node)
    builder.add_node("script_refinement_node", script_refinement_node)

    builder.add_edge(START, "audience_insight_node")
    builder.add_edge("audience_insight_node", "creative_strategy_node")
    builder.add_edge("creative_strategy_node", "script_generation_node")
    builder.add_edge("script_generation_node", "script_evaluation_node")
    builder.add_conditional_edges(
        "script_evaluation_node",
        route_after_evaluation,
        {
            "script_refinement_node": "script_refinement_node",
            END: END
        }
    )
    builder.add_edge("script_refinement_node", "script_evaluation_node")

    return builder.compile()


def route_after_variation_evaluation(state: AgentState) -> str:
    """Route after variation evaluation - similar to main workflow routing."""
    if state.variation_evaluation_report and state.variation_evaluation_report.is_approved_for_next_stage:
        logger.info("Variation script approved by AI. Moving to finalization.")
        return "finalize_variation_node"

    if state.variation_iteration_count >= MAX_VARIATION_REFINEMENT_ITERATIONS:
        logger.warning(
            f"Max variation refinement iterations ({MAX_VARIATION_REFINEMENT_ITERATIONS}) reached. Finalizing variation.")
        return "finalize_variation_node"
    else:
        logger.info(
            f"Variation script not approved. Iteration {state.variation_iteration_count + 1}/{MAX_VARIATION_REFINEMENT_ITERATIONS}. Sending to refinement.")
        return "variation_refinement_node"


def finalize_variation_node(state: AgentState) -> AgentState:
    """Final node to package the variation result."""
    logger.info("Finalizing single variation result...")

    # Create the final single variation result
    single_variation = SingleVariation(
        variation_name="Enhanced A/B Test Variant",
        variation_type="Hook + CTA + Emotional Tone Enhancement",
        base_script_comparison="Modified opening hook, enhanced call-to-action, and shifted emotional tone for A/B testing against the original script",
        ad_script_variation=state.variation_script_draft,
        variation_evaluation_report=state.variation_evaluation_report,
        variation_iteration_count=state.variation_iteration_count,
        notes=f"Refined through {state.variation_iteration_count} iterations with final quality score of {state.variation_evaluation_report.overall_score:.1f}/5.0" if state.variation_evaluation_report else "Generated single variation for A/B testing"
    )

    return state.model_copy(update={
        "single_variation_result": single_variation
    })


def build_variation_graph():
    """Build the variation workflow graph with evaluation and refinement loop."""
    builder = StateGraph(AgentState)

    # Add nodes
    builder.add_node("variation_generation_node", variation_generation_node)
    builder.add_node("variation_evaluation_node", variation_evaluation_node)
    builder.add_node("variation_refinement_node", variation_refinement_node)
    builder.add_node("finalize_variation_node", finalize_variation_node)

    # Linear flow: START -> generate -> evaluate
    builder.add_edge(START, "variation_generation_node")
    builder.add_edge("variation_generation_node", "variation_evaluation_node")

    # Conditional routing after evaluation
    builder.add_conditional_edges(
        "variation_evaluation_node",
        route_after_variation_evaluation,
        {
            "variation_refinement_node": "variation_refinement_node",
            "finalize_variation_node": "finalize_variation_node"
        }
    )

    # Refinement loop back to evaluation
    builder.add_edge("variation_refinement_node", "variation_evaluation_node")

    # Final step
    builder.add_edge("finalize_variation_node", END)

    return builder.compile()
