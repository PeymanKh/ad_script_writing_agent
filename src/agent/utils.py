# Import libraries
import os
import json
import yaml
from typing import List, Optional, Dict
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage

from src.agent.state import AgentState
from src.agent.prompts import (audience_insight_system_prompt , creative_strategy_system_prompt,
                               script_generation_system_prompt, script_evaluation_system_prompt,
                               script_refinement_system_prompt, variation_generation_system_prompt)


def format_list(items: Optional[List[str]]) -> str:
    if not items:
        return "[not specified]"
    return "\n    - " + "\n    - ".join(items)


def format_dict_as_list(d: Dict[str, str]) -> str:
    if not d:
        return "[not specified]"
    return "\n    - " + "\n    - ".join([f"{k}: {v}" for k, v in d.items()])


def read_yaml_from_parent(filename):
    """
    Read and parse a YAML file located one directory above the script's location.

    Args:
        filename (str): Name of the YAML file (e.g., 'your_file.yaml').

    Returns:
        dict or list: Parsed contents of the YAML file.
    """
    yaml_path = "src/agent/copywriting_guideline.yaml"

    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

guideline = read_yaml_from_parent('copywriting_guideline.yaml')

def build_audience_insight_message(state: AgentState) -> List[BaseMessage]:
    a = state.audience_persona
    p = state.product

    user_content_string = f"""\
### Target Audience Profile ###
{json.dumps(a.model_dump(), indent=2)}

### Product Details ###
{json.dumps(p.model_dump(), indent=2)}
"""

    return [
        SystemMessage(content=audience_insight_system_prompt),
        HumanMessage(content=user_content_string.strip())
    ]


def build_creative_strategy_message(state: AgentState) -> List[BaseMessage]:
    p = state.product
    a = state.audience_persona
    ai = state.audience_insight
    guideline = read_yaml_from_parent('copywriting_guideline.yaml')
    preferred_hook_examples = [
        "Your phone's camera is now your personal chef. Here's how.",
        "What if you could turn THIS [show photo of a delicious dish with cheese and fat] into YOUR weight lose friendly meal?"
        "Sick of recipes that ignore your allergies and fitness goals?",
        "Tired of boring meals that don't fit your diet?",
        "Still searching for a ‘keto, no-nuts’ dinner idea? Watch this...",
        "Post-workout and starving? Let this app pick tonight’s meal while you cool down.",
        "Struggling to find a dish that matches your diet perfectly?",
        "Tired of boring meal preps? See how I made my cravings work for my goals!",
        "What if you could eat THIS and still hit your fitness goals?",
        "Ever wish you could snap a photo and get a healthy recipe made for your goals?"
    ]
    preferred_cta_examples = [
        "Download Delisio and personalize your meals!"
        "Tap to create your first personalized recipe.",
        "Get Delisio and solve dinner tonight.",
        "Install Delisio and start cooking smarter",
        "Install and turn any meal photo into your healthiest dish.",
        "Get your AI personal chef. Tap to install now!",
        "Download Delisio today and take control of your healthy cooking journey."
        "Download Delisio and cook smarter in minutes.",
    ]

    # Create a clean demographic profile by excluding redundant fields
    demographic_profile = {
        "age_range": a.age_range,
        "gender": a.gender.value,
        "location": [c.value for c in a.location],
        "income_range": a.income_range.value,
        "education_level": a.education_level.value if a.education_level else 'Not specified'
    }

    # Prepare a dictionary for the campaign brief and audience insights
    campaign_and_insights_dict = {
        "campaign_brief": {
            "campaign_goal": state.campaign_goal.value,
            "ad_platform": state.ad_platform.value,
            "creative_direction": state.creative_direction.value,
            "script_tone": state.script_tone,
            "product_details": {
                "name": p.product_name,
                "overview": p.product_description,
                "focused_feature": {
                    "name": state.product_feature_focus,
                    "description": p.product_features.get(state.product_feature_focus)
                },
                "unique_selling_points": p.unique_selling_point,
                "problems_solved": p.problems_solved,
                "supported_platforms": [sp.value for sp in p.supported_platforms]
            }
        },
        "demographic_profile": demographic_profile,
        "detailed_audience_insights": ai.model_dump(),
        "preferred_hook_examples": preferred_hook_examples,
        "preferred_cta_examples": preferred_cta_examples
    }

    # Use json.dumps to format the structured data for the LLM
    structured_data_str = json.dumps(campaign_and_insights_dict, indent=2)

    # Combine the structured data with the guidelines
    user_content_string = f"""\
    ### Campaign Brief and Audience Insights ###
    {structured_data_str}

    ### Reels Copywriting Guideline ###
    {yaml.dump(guideline, sort_keys=False)}

    ---
    Generate the JSON creative strategy based on the above information.
    """

    return [
        SystemMessage(content=creative_strategy_system_prompt),
        HumanMessage(content=user_content_string.strip())
    ]


def build_script_generation_message(state: AgentState) -> List[BaseMessage]:
    p = state.product
    a = state.audience_persona
    ai = state.audience_insight
    guideline = read_yaml_from_parent('copywriting_guideline.yaml')

    # Prepare a single, comprehensive dictionary for all inputs
    inputs_dict = {
        "campaign_brief": {
            "campaign_goal": state.campaign_goal.value,
            "ad_platform": state.ad_platform.value,
            "creative_direction": state.creative_direction.value,
            "script_tone": state.script_tone.value,
            "product_details": {
                "name": p.product_name,
                "overview": p.product_description,
                "focused_feature": {
                    "name": state.product_feature_focus,
                    "description": p.product_features.get(state.product_feature_focus)
                },
                "unique_selling_points": p.unique_selling_point,
                "problems_solved": p.problems_solved,
                "supported_platforms": [sp.value for sp in p.supported_platforms]
            }
        },
        "creative_strategy": {
            "core_message_pillars": state.core_message_pillars,
            "brainstormed_hooks": state.brainstormed_hooks,
            "generated_ctas": state.generated_ctas,
            "emotional_triggers": state.emotional_triggers,
            "primary_visual_concept": state.primary_visual_concept,
            "audio_strategy": state.audio_strategy
        },
        "audience_insights": {
            "demographic_profile": {
                "age_range": a.age_range,
                "gender": a.gender.value,
                "location": [c.value for c in a.location],
                "income_range": a.income_range.value,
                "education_level": a.education_level.value if a.education_level else 'Not specified'
            },
            "detailed_insights": ai.model_dump()
        }
    }

    # Use json.dumps to format the entire dictionary
    structured_data_str = json.dumps(inputs_dict, indent=2)

    user_content_string = f"""\
    ### Ad Campaign Inputs ###
    {structured_data_str}

    ### Reels Copywriting Guideline ###
    {yaml.dump(guideline, sort_keys=False)}

    ---
    Generate the JSON creative strategy based on the above information.
    """

    return [
        SystemMessage(content=script_generation_system_prompt),
        HumanMessage(content=user_content_string.strip())
    ]


def build_evaluation_message(state: AgentState) -> List[BaseMessage]:
    # Pre-check: Ensure script_draft exists before evaluation
    if not state.script_draft:
        raise ValueError("Script draft is missing for evaluation.")

    # Create a list of history entries for JSON serialization
    history_list = []
    if state.script_iteration_history:
        for entry in state.script_iteration_history:
            history_list.append({
                "timestamp": entry.get("timestamp", "N/A"),
                "recommendations_given": entry.get("previous_evaluation_report", {}).get("actionable_recommendations",
                                                                                         []),
                "script_produced_key_takeaway": entry.get("output_refined_script", {}).get("key_takeaway"),
                "script_produced_cta": entry.get("output_refined_script", {}).get("call_to_action_text"),
                # You can add more refined script details here if needed
            })

    # Prepare a single, comprehensive dictionary for all inputs
    evaluation_inputs_dict = {
        "campaign_brief": {
            "campaign_goal": state.campaign_goal.value,
            "ad_platform": state.ad_platform.value,
            "creative_direction": state.creative_direction.value,
            "script_tone": state.script_tone.value,
        },
        "product_details": {
            "name": state.product.product_name,
            "overview": state.product.product_description,
            "focused_feature": {
                "name": state.product_feature_focus,
                "description": state.product.product_features.get(state.product_feature_focus)
            },
            "unique_selling_points": state.product.unique_selling_point,
            "problems_solved": state.product.problems_solved,
        },
        "creative_strategy": {
            "core_message_pillars": state.core_message_pillars,
            "brainstormed_hooks": state.brainstormed_hooks,
            "generated_ctas": state.generated_ctas,
            "emotional_triggers": state.emotional_triggers,
        },
        "audience_insights": {
            "demographic_profile": {
                "age_range": state.audience_persona.age_range,
                "gender": state.audience_persona.gender.value,
                "location": [c.value for c in state.audience_persona.location],
                "income_range": state.audience_persona.income_range.value,
                "education_level": state.audience_persona.education_level.value if state.audience_persona.education_level else 'Not specified'
            },
            "detailed_insights": state.audience_insight.model_dump()
        },
        "script_refinement_history": history_list
    }

    # Use json.dumps to format the entire dictionary
    structured_data_str = json.dumps(evaluation_inputs_dict, indent=2)

    # Load the copywriting guidelines
    guideline = read_yaml_from_parent('copywriting_guideline.yaml')

    # Construct the final user message string
    user_content_string = f"""\
### Evaluation Context ###
{structured_data_str}

### Reels Copywriting Guideline ###
{yaml.dump(guideline, sort_keys=False)}

---
### Script to Evaluate (Current Version) ###
Below is the ad script generated or refined for review. Analyze it against all the above context, and the evaluation criteria provided in your system prompt.

```json
{state.script_draft.model_dump_json(indent=2)}
"""

    return [
        SystemMessage(content=script_evaluation_system_prompt),
        HumanMessage(content=user_content_string.strip())
    ]


def build_script_refinement_message(state: AgentState) -> List[BaseMessage]:
    # Ensure evaluation report exists before proceeding
    if not state.evaluation_report:
        raise ValueError("Evaluation Report is missing. Cannot build refinement message.")

    # Create a clean list of history entries for JSON serialization
    history_list = []
    if state.script_iteration_history:
        for entry in state.script_iteration_history:
            history_list.append(entry)

    # Create a clean demographic profile
    a = state.audience_persona
    demographic_profile = {
        "age_range": a.age_range,
        "gender": a.gender.value,
        "location": [c.value for c in a.location],
        "income_range": a.income_range.value,
        "education_level": a.education_level.value if a.education_level else 'Not specified'
    }

    # Prepare a single, comprehensive dictionary for all inputs
    refinement_inputs_dict = {
        "campaign_brief": {
            "campaign_goal": state.campaign_goal.value,
            "ad_platform": state.ad_platform.value,
            "creative_direction": state.creative_direction.value,
            "script_tone": state.script_tone.value,
        },
        "product_details": {
            "name": state.product.product_name,
            "overview": state.product.product_description,
            "focused_feature": {
                "name": state.product_feature_focus,
                "description": state.product.product_features.get(state.product_feature_focus)
            },
            "unique_selling_points": state.product.unique_selling_point,
            "problems_solved": state.product.problems_solved,
        },
        "creative_strategy": {
            "core_message_pillars": state.core_message_pillars,
            "brainstormed_hooks": state.brainstormed_hooks,
            "generated_ctas": state.generated_ctas,
            "emotional_triggers": state.emotional_triggers,
        },
        "audience_insights": {
            "demographic_profile": demographic_profile,
            "detailed_insights": state.audience_insight.model_dump()
        },
        "script_refinement_history": history_list,
        "current_script_draft": state.script_draft.model_dump(),
        "evaluation_feedback": state.evaluation_report.model_dump()
    }

    # Use json.dumps to format the entire dictionary
    structured_data_str = json.dumps(refinement_inputs_dict, indent=2)

    # Load the copywriting guidelines
    guideline = read_yaml_from_parent('copywriting_guideline.yaml')

    # Construct the final user message string
    user_content_string = f"""\
### Refinement Context ###
{structured_data_str}

### Reels Copywriting Guideline ###
{yaml.dump(guideline, sort_keys=False)}

---
Based on the above context and the specific recommendations in the `evaluation_feedback` field, generate the refined ad script as a JSON object.
"""
    return [
        SystemMessage(content=script_refinement_system_prompt),
        HumanMessage(content=user_content_string.strip())
    ]

def build_variation_generation_message(state: AgentState) -> List[BaseMessage]:
    # Ensure the script draft has been finalized or approved
    if not state.script_draft:
        raise ValueError("No approved script draft available for variation generation.")

    # Create a clean demographic profile
    a = state.audience_persona
    demographic_profile = {
        "age_range": a.age_range,
        "gender": a.gender.value,
        "location": [c.value for c in a.location],
        "income_range": a.income_range.value,
        "education_level": a.education_level.value if a.education_level else 'Not specified'
    }

    # Prepare a single, comprehensive dictionary for all inputs
    variation_inputs_dict = {
        "campaign_brief": {
            "campaign_goal": state.campaign_goal.value,
            "ad_platform": state.ad_platform.value,
            "creative_direction": state.creative_direction.value,
            "script_tone": state.script_tone.value,
        },
        "product_details": {
            "name": state.product.product_name,
            "overview": state.product.product_description,
            "focused_feature": {
                "name": state.product_feature_focus,
                "description": state.product.product_features.get(state.product_feature_focus)
            },
            "unique_selling_points": state.product.unique_selling_point,
            "problems_solved": state.product.problems_solved,
        },
        "audience_insights": {
            "demographic_profile": demographic_profile,
            "detailed_insights": state.audience_insight.model_dump()
        },
        "approved_base_script": state.script_draft.model_dump(),
    }

    # Use json.dumps to format the entire dictionary
    structured_data_str = json.dumps(variation_inputs_dict, indent=2)

    user_content_string = f"""\
### Ad Campaign Context ###
{structured_data_str}

---
Based on the above approved script, campaign context, and audience insights, generate 3 distinct variants optimized for A/B testing.
"""
    return [
        SystemMessage(content=variation_generation_system_prompt),
        HumanMessage(content=user_content_string.strip())
    ]
