import streamlit as st
import json
from src.agent.state import AgentState
from src.ui_components.display import display_video_script, display_static_script, display_evaluation_scores, \
    display_iteration_history


def safe_get_attribute(obj, attr_name, default=None):
    """Safely get attribute from either object or dictionary."""
    if isinstance(obj, dict):
        return obj.get(attr_name, default)
    else:
        return getattr(obj, attr_name, default)


def safe_get_enum_value(enum_obj, default="Unknown"):
    """Safely get enum value whether it's an enum object or string."""
    if hasattr(enum_obj, 'value'):
        return enum_obj.value
    elif isinstance(enum_obj, str):
        return enum_obj
    else:
        return default


def results_ui():
    st.set_page_config(
        page_title="Ad Script Results",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
    <style>
    /* Hide sidebar completely */
    section[data-testid="stSidebar"] {display: none !important}
    .css-1d391kg {display: none}
    .css-14xtw13.e8zbici0 {display: none}
    .css-15zrgzn {display: none}
    .css-eczf16 {display: none}
    .css-jn99sy {display: none}
    .css-17ziqus {display: none}
    .css-1rs6os {display: none}
    .css-1lcbmhc {display: none}
    .css-1outpf7 {display: none}

    /* Expand main content */
    .main .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: none;
    }
    </style>
    """, unsafe_allow_html=True)


    # Check if we have results
    if 'workflow_result' not in st.session_state:
        st.error("❌ No results found. Please run the workflow first.")
        if st.button("Go Back to Form"):
            st.switch_page("app.py")
        return

    result = st.session_state['workflow_result']

    # Header
    st.title("✅ Your Ad Script is Ready!")
    st.markdown("Here's your AI-generated ad script optimized for your target platform and audience.")

    # Quick stats - handle both AgentState object and dictionary
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        campaign_goal = safe_get_attribute(result, 'campaign_goal')
        goal_display = safe_get_enum_value(campaign_goal).replace('_', ' ').title()
        st.metric("Campaign Goal", goal_display)

    with col2:
        ad_platform = safe_get_attribute(result, 'ad_platform')
        platform_display = safe_get_enum_value(ad_platform).replace('_', ' ').title()
        st.metric("Platform", platform_display)

    with col3:
        iterations = safe_get_attribute(result, 'iteration_count', 0)
        st.metric("Iterations", iterations)

    with col4:
        tokens = safe_get_attribute(result, 'total_llm_tokens', 0)
        st.metric("Tokens Used", f"{tokens:,}")

    st.markdown("---")

    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Final Script", "📊 Quality Scores", "🔄 Process History", "💾 Export"])

    with tab1:
        script_draft = safe_get_attribute(result, 'script_draft')
        if script_draft:
            script_type = safe_get_attribute(script_draft, 'script_type', 'Video')
            if script_type == "Video":
                display_video_script(script_draft)
            else:
                display_static_script(script_draft)
        else:
            st.error("No script was generated.")

    with tab2:
        evaluation_report = safe_get_attribute(result, 'evaluation_report')
        if evaluation_report:
            display_evaluation_scores(evaluation_report)
        else:
            st.info("No evaluation report available.")

    with tab3:
        st.subheader("📈 Workflow Process")

        # Campaign details
        with st.expander("📋 Campaign Configuration", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                product = safe_get_attribute(result, 'product')
                if product:
                    product_name = safe_get_attribute(product, 'product_name', 'Unknown')
                    st.write("**Product:**", product_name)

                product_feature_focus = safe_get_attribute(result, 'product_feature_focus', 'Unknown')
                st.write("**Feature Focus:**", product_feature_focus)

                creative_direction = safe_get_attribute(result, 'creative_direction')
                direction_display = safe_get_enum_value(creative_direction).replace('_', ' ').title()
                st.write("**Creative Direction:**", direction_display)

                script_tone = safe_get_attribute(result, 'script_tone')
                tone_display = safe_get_enum_value(script_tone).replace('_', ' ').title()
                st.write("**Script Tone:**", tone_display)

            with col2:
                st.write("**Target Audience:**")
                audience_persona = safe_get_attribute(result, 'audience_persona')
                if audience_persona:
                    age_range = safe_get_attribute(audience_persona, 'age_range', 'Unknown')
                    st.write(f"• Age: {age_range}")

                    gender = safe_get_attribute(audience_persona, 'gender')
                    gender_display = safe_get_enum_value(gender).title()
                    st.write(f"• Gender: {gender_display}")

                    income_range = safe_get_attribute(audience_persona, 'income_range')
                    income_display = safe_get_enum_value(income_range)
                    st.write(f"• Income: {income_display}")

                    location = safe_get_attribute(audience_persona, 'location', [])
                    if location:
                        if isinstance(location[0], str):
                            location_display = ', '.join([c.upper() for c in location])
                        else:
                            location_display = ', '.join([c.value.upper() for c in location])
                        st.write(f"• Location: {location_display}")

        # Audience insights
        audience_insight = safe_get_attribute(result, 'audience_insight')
        if audience_insight:
            with st.expander("🎯 Audience Insights Generated", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    common_interests = safe_get_attribute(audience_insight, 'common_interests', [])
                    st.write("**Common Interests:**")
                    for interest in common_interests:
                        st.write(f"• {interest}")

                    core_values = safe_get_attribute(audience_insight, 'core_values_and_beliefs', [])
                    st.write("**Core Values:**")
                    for value in core_values:
                        st.write(f"• {value}")

                with col2:
                    pain_points = safe_get_attribute(audience_insight, 'elaborated_pain_points', [])
                    st.write("**Pain Points:**")
                    for pain in pain_points:
                        st.write(f"• {pain}")

                    aspirations = safe_get_attribute(audience_insight, 'elaborated_aspiration_outcomes', [])
                    st.write("**Aspirations:**")
                    for aspiration in aspirations:
                        st.write(f"• {aspiration}")

        # Creative strategy
        brainstormed_hooks = safe_get_attribute(result, 'brainstormed_hooks')
        if brainstormed_hooks:
            with st.expander("💡 Creative Strategy Generated", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Generated Hooks:**")
                    for hook in brainstormed_hooks:
                        st.write(f"• {hook}")

                    core_message_pillars = safe_get_attribute(result, 'core_message_pillars', [])
                    st.write("**Core Messages:**")
                    for msg in core_message_pillars:
                        st.write(f"• {msg}")

                with col2:
                    generated_ctas = safe_get_attribute(result, 'generated_ctas', [])
                    st.write("**Call-to-Actions:**")
                    for cta in generated_ctas:
                        st.write(f"• {cta}")

                    emotional_triggers = safe_get_attribute(result, 'emotional_triggers', [])
                    st.write("**Emotional Triggers:**")
                    for trigger in emotional_triggers:
                        st.write(f"• {trigger}")

        # Iteration history
        iteration_history = safe_get_attribute(result, 'script_iteration_history')
        display_iteration_history(iteration_history)

    with tab4:
        st.subheader("💾 Export Your Script")
        st.markdown("Download your ad script in various formats:")

        # Prepare export data - safely handle both object and dict formats
        product = safe_get_attribute(result, 'product')
        script_draft = safe_get_attribute(result, 'script_draft')
        evaluation_report = safe_get_attribute(result, 'evaluation_report')

        export_data = {
            "campaign_config": {
                "goal": safe_get_enum_value(safe_get_attribute(result, 'campaign_goal')),
                "platform": safe_get_enum_value(safe_get_attribute(result, 'ad_platform')),
                "creative_direction": safe_get_enum_value(safe_get_attribute(result, 'creative_direction')),
                "tone": safe_get_enum_value(safe_get_attribute(result, 'script_tone')),
            },
            "product": {
                "name": safe_get_attribute(product, 'product_name', 'Unknown') if product else 'Unknown',
                "description": safe_get_attribute(product, 'product_description', 'Unknown') if product else 'Unknown',
                "feature_focus": safe_get_attribute(result, 'product_feature_focus', 'Unknown'),
            } if product else {},
            "script": safe_get_attribute(script_draft, '__dict__', script_draft) if script_draft else None,
            "evaluation": safe_get_attribute(evaluation_report, '__dict__',
                                             evaluation_report) if evaluation_report else None,
            "metadata": {
                "iterations": safe_get_attribute(result, 'iteration_count', 0),
                "tokens_used": safe_get_attribute(result, 'total_llm_tokens', 0),
                "generated_at": safe_get_attribute(result, 'timestamp', 'Unknown'),
            }
        }

        col1, col2 = st.columns(2)

        with col1:
            # JSON export
            json_data = json.dumps(export_data, indent=2, default=str)
            product_name = safe_get_attribute(product, 'product_name', 'ad_script') if product else 'ad_script'
            filename = f"ad_script_{product_name.lower().replace(' ', '_')}.json"
            st.download_button(
                label="📄 Download as JSON",
                data=json_data,
                file_name=filename,
                mime="application/json"
            )

        with col2:
            # Text export
            if script_draft:
                script_type = safe_get_attribute(script_draft, 'script_type', 'Video')
                product_name = safe_get_attribute(product, 'product_name',
                                                  'Unknown Product') if product else 'Unknown Product'

                if script_type == "Video":
                    text_content = f"""AD SCRIPT: {product_name}
Platform: {safe_get_enum_value(safe_get_attribute(result, 'ad_platform'))}
Duration: {safe_get_attribute(script_draft, 'duration_estimate_seconds', 'Unknown')}s

SCENES:
"""
                    scenes = safe_get_attribute(script_draft, 'scenes', [])
                    for scene in scenes:
                        scene_number = safe_get_attribute(scene, 'scene_number', 'Unknown')
                        duration = safe_get_attribute(scene, 'duration_seconds', 'Unknown')
                        visual = safe_get_attribute(scene, 'visual_description', 'No description')
                        audio = safe_get_attribute(scene, 'audio_description', 'No description')

                        text_content += f"""
Scene {scene_number} ({duration}s):
Visual: {visual}
Audio: {audio}
"""
                        voiceover = safe_get_attribute(scene, 'voiceover_dialogue')
                        if voiceover:
                            text_content += f"Voiceover: {voiceover}\n"

                        on_screen_text = safe_get_attribute(scene, 'on_screen_text')
                        if on_screen_text:
                            text_content += f"On-Screen Text: {on_screen_text}\n"

                else:
                    text_content = f"""AD SCRIPT: {product_name}
Platform: {safe_get_enum_value(safe_get_attribute(result, 'ad_platform'))}

HEADLINE: {safe_get_attribute(script_draft, 'headline', 'No headline')}

BODY COPY:
{safe_get_attribute(script_draft, 'body_copy', 'No body copy')}

IMAGE DESCRIPTION:
{safe_get_attribute(script_draft, 'image_description', 'No image description')}

ON-IMAGE TEXT:
{safe_get_attribute(script_draft, 'on_image_text', 'No on-image text')}
"""

                cta_text = safe_get_attribute(script_draft, 'call_to_action_text', 'No CTA')
                hashtags = safe_get_attribute(script_draft, 'suggested_hashtags', [])
                key_takeaway = safe_get_attribute(script_draft, 'key_takeaway', 'No key takeaway')

                text_content += f"""

CALL TO ACTION: {cta_text}

HASHTAGS: {' '.join([tag for tag in hashtags])}

KEY TAKEAWAY: {key_takeaway}
"""

                filename = f"ad_script_{product_name.lower().replace(' ', '_')}.txt"
                st.download_button(
                    label="📝 Download as Text",
                    data=text_content,
                    file_name=filename,
                    mime="text/plain"
                )

    # Action buttons
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🧪 Generate A/B Variants", use_container_width=True):
            st.switch_page("pages/variations.py")

    with col2:
        if st.button("🔄 Generate New Script", use_container_width=True):
            # Clear session state and go back to form
            keys_to_clear = ['agent_state', 'workflow_result', 'processing_started', 'processing_complete',
                             'processing_error']
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            st.switch_page("app.py")

    with col3:
        if st.button("✏️ Modify Inputs", use_container_width=True):
            # Keep the workflow result but go back to form
            st.switch_page("app.py")

    with col4:
        if st.button("🔄 Rerun Workflow", use_container_width=True):
            # Keep agent state but clear results
            keys_to_clear = ['workflow_result', 'processing_started', 'processing_complete', 'processing_error']
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            st.switch_page("pages/processing.py")


if __name__ == "__main__":
    results_ui()
