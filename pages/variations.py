import streamlit as st
import time
from src.agent.graph import build_variation_graph
from src.agent.state import AgentState
from src.ui_components.display import display_video_script, display_static_script


def variations_ui():
    st.set_page_config(
        page_title="A/B Testing Variations",
        layout="wide",
        initial_sidebar_state="collapsed",
        page_icon="🧪"
    )

    # Hide sidebar CSS
    st.markdown("""
    <style>
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

    /* Dark theme styling */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
    }

    .stApp {
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
    }

    .main .block-container {
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: none;
        background-color: #0f172a !important;
    }

    /* Beautiful header */
    .variations-header {
        text-align: center;
        padding: 2rem 0 3rem 0;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border-radius: 20px;
        margin-bottom: 3rem;
        color: white;
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
    }

    .variations-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }

    .variations-header p {
        font-size: 1.1rem;
        font-weight: 400;
        opacity: 0.9;
        margin-bottom: 0;
    }

    /* Variant cards */
    .variant-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        border: 1px solid #475569;
        transition: all 0.3s ease;
    }

    .variant-card:hover {
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.2);
        transform: translateY(-2px);
        border-color: #6366f1;
    }

    .variant-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
    }

    .variant-badge {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin-right: 1rem;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
    }

    .variant-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #f1f5f9 !important;
        margin: 0;
    }

    /* Progress animation */
    .generating-animation {
        text-align: center;
        padding: 3rem 0;
    }

    .spinner {
        width: 50px;
        height: 50px;
        border: 4px solid #334155;
        border-top: 4px solid #6366f1;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 1rem;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.6);
    }

    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #1e40af 0%, #3730a3 100%) !important;
        border: 1px solid #3b82f6;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        color: #dbeafe !important;
    }

    /* Metrics styling */
    .stMetric {
        background: rgba(51, 65, 85, 0.5) !important;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #475569;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #334155;
        color: #e2e8f0;
        border-radius: 8px;
        border: 1px solid #475569;
    }

    .stTabs [aria-selected="true"] {
        background-color: #6366f1 !important;
        color: white !important;
    }

    p, span, div {
        color: #e2e8f0 !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #f1f5f9 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Check if we have the required workflow result
    if 'workflow_result' not in st.session_state:
        st.error("❌ No base script found. Please generate a script first.")
        if st.button("🔙 Go Back to Main Page"):
            st.switch_page("app.py")
        return

    # Header
    st.markdown("""
    <div class="variations-header">
        <h1>🧪 A/B Testing Variations</h1>
        <p>Generate multiple script variants optimized for different audience segments and testing scenarios</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize variation states
    if 'variations_generated' not in st.session_state:
        st.session_state['variations_generated'] = False
        st.session_state['variations_result'] = None
        st.session_state['generating_variations'] = False

    # Base script info
    base_result = st.session_state['workflow_result']

    # Display base script summary
    st.subheader("📄 Original Base Script")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if isinstance(base_result, dict):
            campaign_goal = base_result.get('campaign_goal', 'Unknown')
            goal_display = campaign_goal.value if hasattr(campaign_goal, 'value') else str(campaign_goal)
        else:
            goal_display = base_result.campaign_goal.value if hasattr(base_result.campaign_goal, 'value') else str(
                base_result.campaign_goal)
        st.metric("Campaign Goal", goal_display.replace('_', ' ').title())

    with col2:
        if isinstance(base_result, dict):
            ad_platform = base_result.get('ad_platform', 'Unknown')
            platform_display = ad_platform.value if hasattr(ad_platform, 'value') else str(ad_platform)
        else:
            platform_display = base_result.ad_platform.value if hasattr(base_result.ad_platform, 'value') else str(
                base_result.ad_platform)
        st.metric("Platform", platform_display.replace('_', ' ').title())

    with col3:
        if isinstance(base_result, dict):
            script_draft = base_result.get('script_draft')
        else:
            script_draft = base_result.script_draft

        script_type = "Video" if script_draft and (
            script_draft.get('script_type') == 'Video' if isinstance(script_draft, dict) else getattr(script_draft,
                                                                                                      'script_type',
                                                                                                      'Video') == 'Video') else "Static"
        st.metric("Script Type", script_type)

    with col4:
        if isinstance(base_result, dict):
            eval_report = base_result.get('evaluation_report')
        else:
            eval_report = base_result.evaluation_report

        if eval_report:
            overall_score = eval_report.get('overall_score', 0) if isinstance(eval_report,
                                                                              dict) else eval_report.overall_score
            st.metric("Base Quality Score", f"{overall_score:.1f}/5.0")
        else:
            st.metric("Base Quality Score", "N/A")

    # Full Base Script Display with Toggle
    st.markdown("### 🎯 Complete Base Script")

    with st.expander("📋 View Full Base Script", expanded=True):
        # Style the base script with a special container
        st.markdown("""
        <div style="padding: 1.5rem; border: 2px solid #22c55e; border-radius: 16px; background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(22, 163, 74, 0.15) 100%); margin: 1rem 0; box-shadow: 0 4px 20px rgba(34, 197, 94, 0.2);">
            <div style="display: flex; align-items: center; margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px solid rgba(34, 197, 94, 0.3);">
                <div style="background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color: white; padding: 0.5rem 1rem; border-radius: 25px; font-weight: 600; font-size: 0.95rem; margin-right: 1rem; box-shadow: 0 4px 12px rgba(34, 197, 94, 0.4);">✅ ORIGINAL</div>
                <h3 style="color: #f1f5f9; margin: 0; font-size: 1.4rem; font-weight: 600;">Base Script (Approved)</h3>
            </div>
            <div style="background: rgba(15, 23, 42, 0.6); padding: 1rem; border-radius: 12px; border: 1px solid rgba(34, 197, 94, 0.3);">
                <p style="color: #94a3b8; margin: 0; font-size: 0.9rem; text-align: center;">📊 This is your original approved script that will be used as the base for generating A/B test variations</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Display the full base script
        if script_draft:
            if isinstance(script_draft, dict):
                script_type = script_draft.get('script_type', 'Video')
            else:
                script_type = getattr(script_draft, 'script_type', 'Video')

            if script_type == "Video":
                display_video_script(script_draft)
            else:
                display_static_script(script_draft)
        else:
            st.error("❌ No base script found to display.")

    st.markdown("---")

    # Info box about A/B testing
    st.markdown("""
    <div class="info-box">
        <strong>🎯 A/B Testing Strategy:</strong> We'll generate 3 distinct variants of your approved script:
        <br><br>
        <strong>• Hook-Focused Variant:</strong> Leads with different pain points or aspirations
        <br><strong>• CTA-Focused Variant:</strong> Features stronger, more urgent calls-to-action
        <br><strong>• Emotional/Tonal Variant:</strong> Uses different emotional triggers and tone
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Generate variations button
    if not st.session_state['variations_generated'] and not st.session_state['generating_variations']:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🧪 Generate A/B Testing Variations", type="primary", use_container_width=True):
                st.session_state['generating_variations'] = True
                st.rerun()

    # Show generation progress
    if st.session_state['generating_variations'] and not st.session_state['variations_generated']:
        st.markdown("""
        <div class="generating-animation">
            <div class="spinner"></div>
            <h3>🤖 AI is creating your A/B testing variants...</h3>
            <p>Analyzing audience insights and generating targeted variations</p>
        </div>
        """, unsafe_allow_html=True)

        try:
            with st.spinner("Generating variations..."):
                # Build and run the variation graph
                variation_graph = build_variation_graph()

                # Convert base result to AgentState if needed
                if isinstance(base_result, dict):
                    try:
                        agent_state = AgentState(**base_result)
                    except:
                        # If conversion fails, create a minimal state
                        agent_state = base_result
                else:
                    agent_state = base_result

                # Generate variations
                result = variation_graph.invoke(agent_state)

                # Store results
                st.session_state['variations_result'] = result
                st.session_state['variations_generated'] = True
                st.session_state['generating_variations'] = False

                st.success("✅ Variations generated successfully!")
                time.sleep(1)
                st.rerun()

        except Exception as e:
            st.error(f"❌ Error generating variations: {str(e)}")
            st.session_state['generating_variations'] = False
            st.rerun()

    # Display generated variations
    if st.session_state['variations_generated'] and st.session_state['variations_result']:
        st.subheader("🎭 Generated Variations")

        variations_result = st.session_state['variations_result']

        # Get final script variants
        if isinstance(variations_result, dict):
            final_variants = variations_result.get('final_scripts_variants')
        else:
            final_variants = getattr(variations_result, 'final_scripts_variants', None)

        if final_variants:
            # Get the variants list
            if hasattr(final_variants, 'final_scripts_variants'):
                variants_list = final_variants.final_scripts_variants
            elif isinstance(final_variants, dict):
                variants_list = final_variants.get('final_scripts_variants', [])
            else:
                variants_list = final_variants

            # Display each variant
            for i, variant in enumerate(variants_list):
                variant_name = variant.variant_name if hasattr(variant, 'variant_name') else variant.get('variant_name',
                                                                                                         f'Variant {i + 1}')
                variant_type = variant.variant_type if hasattr(variant, 'variant_type') else variant.get('variant_type',
                                                                                                         'Unknown')
                variant_notes = variant.notes if hasattr(variant, 'notes') else variant.get('notes', '')

                st.markdown(f"""
                <div class="variant-card">
                    <div class="variant-header">
                        <div class="variant-badge">{variant_type}</div>
                        <h3 class="variant-title">{variant_name}</h3>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Display variant notes
                if variant_notes:
                    st.markdown(f"**📝 Strategy:** {variant_notes}")

                # Display the script
                variant_script = variant.ad_script if hasattr(variant, 'ad_script') else variant.get('ad_script')

                if variant_script:
                    script_type = variant_script.get('script_type', 'Video') if isinstance(variant_script,
                                                                                           dict) else getattr(
                        variant_script, 'script_type', 'Video')

                    if script_type == "Video":
                        display_video_script(variant_script)
                    else:
                        display_static_script(variant_script)

                st.markdown("---")

            # Action buttons
            st.subheader("🚀 Next Steps")
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("🔄 Generate New Variations", use_container_width=True):
                    st.session_state['variations_generated'] = False
                    st.session_state['variations_result'] = None
                    st.rerun()

            with col2:
                if st.button("📊 Back to Results", use_container_width=True):
                    st.switch_page("pages/results.py")

            with col3:
                if st.button("🏠 New Campaign", use_container_width=True):
                    # Clear all session state
                    keys_to_clear = ['agent_state', 'workflow_result', 'variations_generated', 'variations_result']
                    for key in keys_to_clear:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.switch_page("app.py")

        else:
            st.error("❌ No variations were generated. Please try again.")


if __name__ == "__main__":
    variations_ui()
