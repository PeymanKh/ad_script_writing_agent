import streamlit as st
from src.agent.state import VideoScriptDraft, StaticAdDraft, EvaluationReport


def display_video_script(script: VideoScriptDraft):
    """Display a video script in a formatted way."""
    st.subheader("📹 Video Ad Script")

    # Basic info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Platform", script.ad_platform_target.replace('_', ' ').title())
    with col2:
        st.metric("Duration", f"{script.duration_estimate_seconds}s")
    with col3:
        st.metric("Scenes", len(script.scenes))

    st.markdown("---")

    # Scenes
    st.subheader("🎬 Scenes")
    for scene in script.scenes:
        with st.expander(f"Scene {scene.scene_number} ({scene.duration_seconds}s)", expanded=True):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Visual Description:**")
                st.write(scene.visual_description)

                if scene.on_screen_text:
                    st.markdown("**On-Screen Text:**")
                    st.info(scene.on_screen_text)

            with col2:
                st.markdown("**Audio Description:**")
                st.write(scene.audio_description)

                if scene.voiceover_dialogue:
                    st.markdown("**Voiceover/Dialogue:**")
                    st.write(scene.voiceover_dialogue)

    # CTA and hashtags
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎯 Call to Action")
        st.success(script.call_to_action_text)

    with col2:
        st.subheader("🏷️ Suggested Hashtags")
        hashtag_text = " ".join([f"#{tag}" for tag in script.suggested_hashtags])
        st.code(hashtag_text)

    # Key takeaway
    st.subheader("💡 Key Takeaway")
    st.info(script.key_takeaway)


def display_static_script(script: StaticAdDraft):
    """Display a static ad script in a formatted way."""
    st.subheader("📱 Static Ad Script")

    # Basic info
    st.metric("Platform", script.ad_platform_target.replace('_', ' ').title())

    st.markdown("---")

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📝 Ad Copy")

        st.markdown("**Headline:**")
        st.markdown(f"# {script.headline}")

        st.markdown("**Body Copy:**")
        st.write(script.body_copy)

        st.markdown("**Call to Action:**")
        st.success(script.call_to_action_text)

    with col2:
        st.subheader("🖼️ Visual Elements")

        st.markdown("**Image Description:**")
        st.write(script.image_description)

        if script.on_image_text:
            st.markdown("**Text on Image:**")
            st.info(script.on_image_text)

        st.markdown("**Hashtags:**")
        hashtag_text = " ".join([f"#{tag}" for tag in script.suggested_hashtags])
        st.code(hashtag_text)

    # Key takeaway
    st.markdown("---")
    st.subheader("💡 Key Takeaway")
    st.info(script.key_takeaway)


def display_evaluation_scores(evaluation: EvaluationReport):
    """Display evaluation scores in a formatted way."""
    st.subheader("📊 Quality Evaluation")

    # Overall score
    col1, col2 = st.columns([1, 2])
    with col1:
        score_color = "green" if evaluation.overall_score >= 4.0 else "orange" if evaluation.overall_score >= 3.0 else "red"
        st.metric("Overall Score", f"{evaluation.overall_score:.1f}/5.0")

    with col2:
        approval_status = "✅ Approved" if evaluation.is_approved_for_next_stage else "🔄 Needs Refinement"
        st.success(approval_status) if evaluation.is_approved_for_next_stage else st.warning(approval_status)

    st.markdown("---")

    # Detailed scores
    st.subheader("📋 Detailed Scores")

    # Create score grid
    criteria_items = list(evaluation.detailed_scores.items())
    num_cols = 2

    for i in range(0, len(criteria_items), num_cols):
        cols = st.columns(num_cols)

        for j, col in enumerate(cols):
            if i + j < len(criteria_items):
                criterion, metric = criteria_items[i + j]

                with col:
                    # Score with color coding
                    score = metric.score
                    score_color = "🟢" if score >= 4 else "🟡" if score >= 3 else "🔴"

                    st.markdown(f"**{criterion.value.replace('_', ' ').title()}**")
                    st.markdown(f"{score_color} {score}/5")

                    with st.expander("View Feedback"):
                        st.write(metric.feedback)

    # Summary feedback
    st.markdown("---")
    st.subheader("📝 Summary Feedback")
    st.info(evaluation.summary_feedback)

    # Recommendations
    if evaluation.actionable_recommendations:
        st.subheader("🔧 Recommendations")
        for i, rec in enumerate(evaluation.actionable_recommendations, 1):
            st.write(f"{i}. {rec}")


def display_iteration_history(history):
    """Display script iteration history."""
    if not history:
        st.info("No iteration history available.")
        return

    st.subheader("🔄 Refinement History")

    for i, entry in enumerate(history):
        with st.expander(f"Iteration {i + 1} - {entry.get('timestamp', 'Unknown time')}"):
            if 'previous_evaluation_report' in entry:
                prev_eval = entry['previous_evaluation_report']
                st.write(f"**Previous Score:** {prev_eval.get('overall_score', 'N/A')}/5.0")

                if 'actionable_recommendations' in prev_eval:
                    st.write("**Recommendations Implemented:**")
                    for rec in prev_eval['actionable_recommendations']:
                        st.write(f"• {rec}")
