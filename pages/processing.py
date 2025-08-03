import streamlit as st
import time

from src.agent.graph import build_pre_review_graph
from src.agent.state import AgentState


def processing_ui():
    st.set_page_config(
        page_title="Processing Ad Script",
        layout="wide",
        initial_sidebar_state="collapsed"
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

    st.title("🤖 Generating Your Ad Script...")
    st.markdown("Please wait while our AI agents work on your script. This may take 2-5 minutes.")

    # Check if we have the required state
    if 'agent_state' not in st.session_state:
        st.error("No campaign data found. Please go back and fill out the form.")
        if st.button("Go Back to Form"):
            st.switch_page("app.py")
        return

    # Initialize processing status
    if 'processing_started' not in st.session_state:
        st.session_state['processing_started'] = False
        st.session_state['processing_complete'] = False
        st.session_state['processing_error'] = None
        st.session_state['current_step'] = 0
        st.session_state['workflow_result'] = None

    # Progress tracking
    steps = [
        ("🔍 Analyzing Audience", "Understanding your target audience psychology and behaviour"),
        ("💡 Creating Strategy", "Developing effective strategy for your target audience"),
        ("✍️ Writing Script", "Generating your ad script"),
        ("⚖️ Evaluating Quality", "Checking script quality and effectiveness"),
        ("🔧 Refining Script", "Improving script based on evaluation")
    ]

    # Create progress container
    progress_container = st.container()
    with progress_container:
        st.subheader("Workflow Progress")

        current_step = st.session_state.get('current_step', 0)

        # Overall progress bar
        if st.session_state.get('processing_complete'):
            overall_progress = 1.0
        else:
            overall_progress = current_step / len(steps)

        st.progress(overall_progress)

        # Individual step status
        for i, (title, description) in enumerate(steps):
            col1, col2, col3 = st.columns([1, 3, 6])

            with col1:
                if i < current_step:
                    st.write("✅")
                elif i == current_step and st.session_state.get('processing_started'):
                    st.write("🔄")
                else:
                    st.write("⏳")

            with col2:
                if i == current_step and st.session_state.get('processing_started'):
                    st.write(f"**{title}**...")
                else:
                    st.write(f"**{title}**")

            with col3:
                st.write(description)

    # Status messages
    status_container = st.container()

    # Start processing if not started
    if not st.session_state['processing_started']:
        with st.spinner("Initializing workflow..."):
            time.sleep(30)
        st.session_state['processing_started'] = True
        st.rerun()

    # Run the workflow with simulated progress
    if st.session_state['processing_started'] and not st.session_state['processing_complete'] and not st.session_state[
        'processing_error']:

        try:
            with status_container:
                st.info("🚀 Workflow is running... This may take several minutes.")

            # Step 1: Analyzing Audience
            if st.session_state['current_step'] == 0:
                st.session_state['current_step'] = 1
                st.rerun()

            # Step 2: Creating Strategy
            elif st.session_state['current_step'] == 1:
                time.sleep(30)  # Show progress for a moment
                st.session_state['current_step'] = 2
                st.rerun()

            # Step 3: Writing Script
            elif st.session_state['current_step'] == 2:
                time.sleep(30)
                st.session_state['current_step'] = 3
                st.rerun()

            # Step 4: Evaluating Quality
            elif st.session_state['current_step'] == 3:
                time.sleep(30)
                st.session_state['current_step'] = 4
                st.rerun()

            # Final step: Run the actual workflow
            elif st.session_state['current_step'] == 4:
                with st.spinner("Finalizing your ad script..."):
                    # Build and run the graph
                    graph = build_pre_review_graph()
                    agent_state = st.session_state['agent_state']

                    # Run the workflow
                    result_dict = graph.invoke(agent_state)

                    # Convert dictionary back to AgentState object
                    try:
                        result = AgentState(**result_dict)
                    except Exception:
                        result = result_dict

                    # Store result
                    st.session_state['workflow_result'] = result
                    st.session_state['processing_complete'] = True
                    st.session_state['current_step'] = len(steps)

                st.rerun()

        except Exception as e:
            st.session_state['processing_error'] = str(e)
            st.rerun()

    # Handle completion (rest of your existing code...)
    if st.session_state['processing_complete']:
        with status_container:
            st.success("🎉 Your ad script has been generated successfully!")

            result = st.session_state['workflow_result']

            # Quick preview - handle both AgentState object and dictionary
            col1, col2 = st.columns(2)
            with col1:
                if isinstance(result, dict):
                    iterations = result.get('iteration_count', 0)
                else:
                    iterations = result.iteration_count
                st.metric("Total Iterations", iterations)

            with col2:
                if isinstance(result, dict):
                    tokens = result.get('total_llm_tokens', 0)
                else:
                    tokens = result.total_llm_tokens
                st.metric("LLM Tokens Used", f"{tokens:,}")

            # Evaluation report handling
            if isinstance(result, dict):
                eval_report = result.get('evaluation_report')
            else:
                eval_report = result.evaluation_report

            if eval_report:
                if isinstance(eval_report, dict):
                    overall_score = eval_report.get('overall_score', 0)
                else:
                    overall_score = eval_report.overall_score
                st.metric("Overall Quality Score", f"{overall_score:.1f}/5.0")

        st.markdown("---")

        if st.button("View Your Ad Script 📄", type="primary", use_container_width=True):
            st.switch_page("pages/results.py")

    # Handle errors
    if st.session_state['processing_error']:
        with status_container:
            st.error(f"❌ An error occurred during processing:")
            st.code(st.session_state['processing_error'])

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Try Again"):
                    # Reset processing state
                    st.session_state['processing_started'] = False
                    st.session_state['processing_complete'] = False
                    st.session_state['processing_error'] = None
                    st.session_state['current_step'] = 0
                    st.rerun()

            with col2:
                if st.button("Go Back to Form"):
                    st.switch_page("app.py")


if __name__ == "__main__":
    processing_ui()
