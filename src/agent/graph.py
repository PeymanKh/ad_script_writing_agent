from langgraph.graph import StateGraph, START, END

from src.agent.state import AgentState
from src.config.logging_config import get_logger

from src.agent.nodes.audience_insight import audience_insight_node
from src.agent.nodes.creative_strategy import creative_strategy_node
from src.agent.nodes.script_generator import script_generation_node
from src.agent.nodes.script_evaluator import script_evaluation_node
from src.agent.nodes.script_refiner import script_refinement_node
from src.agent.nodes.variation_generator import variation_generation_node

logger = get_logger(__name__)

MAX_REFINEMENT_ITERATIONS = 3

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


def build_variation_graph():
    """Build a simple graph with just the variation generation node."""
    builder = StateGraph(AgentState)

    # Add the variation generation node
    builder.add_node("variation_generation_node", variation_generation_node)

    # Simple linear flow: START -> variation_generation_node -> END
    builder.add_edge(START, "variation_generation_node")
    builder.add_edge("variation_generation_node", END)

    return builder.compile()
