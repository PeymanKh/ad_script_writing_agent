import traceback
import streamlit as st
from datetime import datetime

from src.ui_components.utils import format_enum_value
from src.ui_components.forms import dynamic_list_input
from src.agent.state import (CampaignGoal, AdPlatform, Product, SupportedPlatform,
                             CreativeDirection, ScriptTone, Gender, Countries,
                             IncomeRange, EducationLevel, AudiencePersona, AgentState, )


def initial_input_ui():
    """
    Renders the initial form for the user to input campaign details.
    """
    st.set_page_config(
        page_title="AI Ad Script Generator",
        layout="wide",
        initial_sidebar_state="collapsed",
        page_icon="🚀"
    )

    # Enhanced CSS with modern design
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

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

    /* DARK THEME IMPLEMENTATION */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
    }

    /* Main app dark background */
    .stApp {
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
    }

    /* Main container dark background */
    .main .block-container {
        padding-left: 2rem;
        padding-right: 2rem;
        padding-top: 2rem;
        max-width: none;
        background-color: #0f172a !important;
    }

    /* Header styling - Dark theme */
    .main-header {
        text-align: center;
        padding: 2rem 0 3rem 0;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        border-radius: 20px;
        margin-bottom: 3rem;
        color: white;
        box-shadow: 0 10px 30px rgba(79, 70, 229, 0.3);
    }

    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }

    .main-header p {
        font-size: 1.2rem;
        font-weight: 400;
        opacity: 0.9;
        margin-bottom: 0;
    }

    /* Section cards - Dark theme */
    .section-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        border: 1px solid #475569;
        transition: all 0.3s ease;
    }

    .section-card:hover {
        box-shadow: 0 8px 30px rgba(79, 70, 229, 0.2);
        transform: translateY(-2px);
        border-color: #4f46e5;
    }

    .section-header {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
    }

    .section-number {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 1.1rem;
        margin-right: 1rem;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
    }

    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #f1f5f9 !important;
        margin: 0;
    }

    .section-subtitle {
        font-size: 1rem;
        color: #94a3b8 !important;
        margin-top: 0.25rem;
        margin-bottom: 0;
    }

    /* Progress indicator - Dark theme */
    .progress-steps {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
        padding: 1rem;
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        border-radius: 12px;
        border: 1px solid #475569;
    }

    .step {
        display: flex;
        align-items: center;
        color: #94a3b8;
        font-weight: 500;
    }

    .step.active {
        color: #a855f7;
        font-weight: 600;
    }

    .step-circle {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #64748b;
        margin-right: 0.5rem;
    }

    .step.active .step-circle {
        background: #a855f7;
        box-shadow: 0 0 0 4px rgba(168, 85, 247, 0.2);
    }

    .step-connector {
        width: 50px;
        height: 2px;
        background: #475569;
        margin: 0 1rem;
    }

    /* Form elements - Dark theme */
    .stSelectbox label, .stTextInput label, .stTextArea label, .stMultiSelect label {
        font-weight: 500 !important;
        color: #e2e8f0 !important;
        font-size: 0.95rem !important;
    }

    .stSelectbox > div > div, .stTextInput > div > div, .stTextArea > div > div, .stMultiSelect > div > div {
        border-radius: 8px;
        border: 1.5px solid #475569;
        transition: all 0.2s ease;
        background-color: #334155 !important;
        color: #e2e8f0 !important;
    }

    .stSelectbox > div > div:focus-within, .stTextInput > div > div:focus-within, .stTextArea > div > div:focus-within {
        border-color: #4f46e5;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
    }

    /* Input text color */
    .stSelectbox select, .stTextInput input, .stTextArea textarea {
        color: #e2e8f0 !important;
        background-color: #334155 !important;
    }

    /* Container backgrounds */
    .element-container {
        background-color: transparent !important;
    }

    .stContainer {
        background-color: transparent !important;
    }

    [data-testid="column"] {
        background-color: transparent !important;
    }

    /* Button styling - Dark theme */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.6);
    }

    /* Alert styling - Dark theme */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }

    .stAlert[data-baseweb="notification"] {
        background-color: #7f1d1d !important;
        color: #fecaca !important;
        border-left: 4px solid #ef4444 !important;
    }

    .stSuccess {
        background-color: #14532d !important;
        color: #bbf7d0 !important;
        border-left: 4px solid #22c55e !important;
    }

    /* Info boxes - Dark theme */
    .info-box {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%) !important;
        border: 1px solid #3b82f6;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        color: #dbeafe !important;
    }

    .info-box-icon {
        color: #60a5fa;
        margin-right: 0.5rem;
    }

    /* Divider styling - Dark theme */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #475569, transparent);
        margin: 3rem 0;
    }

    /* Fix any remaining containers */
    .block-container > div {
        background-color: transparent !important;
    }

    .element-container div {
        background-color: transparent !important;
    }

    /* Text colors for dark theme */
    p, span, div {
        color: #e2e8f0 !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #f1f5f9 !important;
    }

    /* Caption text */
    .caption {
        color: #94a3b8 !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

    # Main Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Ad Script Generator Agent</h1>
        <p>Transform your ideas into high-converting social media ad scripts with advanced AI</p>
    </div>
    """, unsafe_allow_html=True)

    # --- 1. Campaign & Creative Details ---
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <div class="section-number">1</div>
            <div>
                <h2 class="section-title">Campaign & Ad Details</h2>
                <p class="section-subtitle">Define the core purpose and target platform for your ad</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown("**🎯 Campaign Goal**")
            campaign_goal = st.selectbox(
                label="Campaign Goal",
                options=[goal.value for goal in CampaignGoal],
                format_func=format_enum_value,
                help="The primary objective of this ad campaign.",
                label_visibility="collapsed"
            )

            st.markdown("**🎨 Creative Direction**")
            creative_direction = st.selectbox(
                label="Creative Direction",
                options=[cd.value for cd in CreativeDirection],
                index=[cd.value for cd in CreativeDirection].index(CreativeDirection.user_generated_content.value),
                format_func=format_enum_value,
                help="The overall messaging angle or creative approach of the ad.",
                label_visibility="collapsed"
            )

        with col2:
            st.markdown("**📱 Ad Platform**")
            ad_platform = st.selectbox(
                label="Ad Platform",
                options=[platform.value for platform in AdPlatform],
                format_func=format_enum_value,
                help="The specific social media placement for the ad.",
                label_visibility="collapsed"
            )

            st.markdown("**🗣️ Script Tone**")
            script_tone = st.selectbox(
                label="Script Tone",
                options=[st.value for st in ScriptTone],
                index=[st.value for st in ScriptTone].index(ScriptTone.friendly.value),
                format_func=format_enum_value,
                help="The requested brand voice or tone for the ad script.",
                label_visibility="collapsed"
            )

    # Info box for campaign section
    st.markdown("""
    <div class="info-box">
        <span class="info-box-icon">💡</span>
        <strong>Pro Tip:</strong> Choose platforms and tones that align with your target audience's preferences. UGC-style content typically performs best on Instagram Reels and TikTok.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # --- 2. Product & Features ---
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <div class="section-number">2</div>
            <div>
                <h2 class="section-title">Product & Features</h2>
                <p class="section-subtitle">Provide details about the mobile app you want to advertise</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns([3, 2], gap="large")

        with col1:
            st.markdown("**📱 Product Name**")
            product_name = st.text_input(
                label="Product Name",
                value="Delisio - Your Personal Chef",
                help="The name of your app.",
                label_visibility="collapsed"
            )

        with col2:
            st.markdown("**🔧 Supported Platforms**")
            supported_platforms = st.multiselect(
                label="Supported Platforms",
                options=[p.value for p in SupportedPlatform],
                default=[SupportedPlatform.ios.value],
                format_func=format_enum_value,
                help="Select all platforms your app supports.",
                label_visibility="collapsed"
            )

        st.markdown("**📝 Product Description**")
        product_description = st.text_area(
            label="Product Description",
            value="Delisio is a personal chef and nutrition assistant. When a user signs up, they enter their age, weight, height, diet (e.g., vegan, keto), nutritional goal (e.g., weight loss, muscle gain), allergies, and cooking skill level. next they can use 3 main features, one is that when they scan a food, Delisio will personalize the reicpe of the food that is healthy and is alligned their unique needs. next is surprise me which creates an unseen recipe from another cuisine, or nation that meets their needs, and finally if they scan their dish, they can see in depth details of the food such as calories, fat, virtamin c, b12, iron, etc...",
            help="A brief overview of your app.",
            height=100,
            label_visibility="collapsed"
        )

        col_features_left, col_features_right = st.columns(2, gap="large")

        with col_features_left:
            st.markdown("**📋 Product Features**")
            st.caption("Enter each feature on a new line in the format: `Feature Name: Description`")
            product_features_raw = st.text_area(
                label="Product Features (Name: Description)",
                value="Photo to Recipe: User uploads a photo of any dish, specify equipments, define calorie preference, and Delisio generates a personalized recipe tailored to their profile.\n"
                      "Name to Recipe: User writes any dish name, specify equipments, define calorie preference, and Delisio generates a personalized recipe tailored to their profile.\n"
                      "Surprise Me: User selects meal type, cuisine, specify equipments, define calorie preference; Delisio generates a unique, personalized recipe (e.g., a vegetarian Chinese breakfast).\n"
                      "Nutrition Scanner: User scans their food; Delisio analyzes and reports nutrients, vitamins, and minerals.\n"
                      "Hydration Tracker: Calculates required daily water intake based on BMI and goals, and help user track their daily water intake.\n",
                height=200,
                label_visibility="collapsed"
            )
            product_features_dict = {}
            for line in product_features_raw.strip().split('\n'):
                if ":" in line:
                    key, value = line.split(":", 1)
                    product_features_dict[key.strip()] = value.strip()

            feature_options = list(product_features_dict.keys())
            if not feature_options:
                feature_options = ["Enter features above first"]

            st.markdown("**⭐ Feature to Focus On**")
            product_feature_focus = st.selectbox(
                label="Feature to Focus On",
                options=feature_options,
                help="Which single feature should the ad highlight?",
                label_visibility="collapsed"
            )

        with col_features_right:
            unique_selling_point = dynamic_list_input(
                label="🚀 Unique Selling Points (USPs)",
                key="usp_list",
                default_value=[
                    "Turn any food image into a personalized, goal-aligned recipe instantly.",
                    "Recipes uniquely tailored to user's body metrics, diet, goals, allergies, and cooking skill.",
                    "Discover new favorite meals, uniquely generated for user's diet and taste.",
                    "Scan any food for instant, detailed nutritional insights (macros, micros, vitamins).",
                    "BMI-based water goals with motivating visual tracking.",
                    "Your all-in-one AI personal chef, nutrition guide, and hydration tracker."
                ]
            )

            problems_solved = dynamic_list_input(
                label="🎯 Problems Solved",
                key="problems_solved_list",
                default_value=[
                    "What should I cook tonight dilemma",
                    "Boredom with repetitive meals",
                    "Difficulty finding recipes that match specific dietary needs/goals",
                    "Uncertainty about food's nutritional content",
                    "Struggling to stay adequately hydrated",
                    "Time constraints for healthy cooking",
                    "Lack of confidence in the kitchen",
                    "Generic health advice that doesn't fit"
                ]
            )

    st.markdown("<hr>", unsafe_allow_html=True)

    # --- 3. Audience Profile ---
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <div class="section-number">3</div>
            <div>
                <h2 class="section-title">Target Audience Profile</h2>
                <p class="section-subtitle">Help the AI understand who you're talking to with a detailed persona</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        # Demographics row
        col1, col2, col3 = st.columns(3, gap="large")

        with col1:
            st.markdown("**👥 Age Range**")
            age_range = st.text_input(
                label="Age Range",
                value="25-33",
                help="Example: '25-33' or '18+'.",
                label_visibility="collapsed"
            )

            st.markdown("**⚧️ Gender**")
            gender = st.selectbox(
                label="Gender",
                options=[g.value for g in Gender],
                format_func=format_enum_value,
                help="Target audience gender.",
                label_visibility="collapsed"
            )

        with col2:
            st.markdown("**🌍 Location**")
            location = st.multiselect(
                label="Location",
                options=[c.value for c in Countries],
                default=[Countries.usa.value, Countries.uk.value, Countries.canada.value],
                format_func=format_enum_value,
                help="Target audience countries.",
                label_visibility="collapsed"
            )

            st.markdown("**💰 Income Range**")
            options_income = [i.value for i in IncomeRange]
            income_range = st.selectbox(
                label="Income Range",
                options=options_income,
                index=options_income.index(IncomeRange.middle.value),
                help="Audience's income category.",
                label_visibility="collapsed"
            )

        with col3:
            st.markdown("**🎓 Education Level**")
            education_level = st.selectbox(
                label="Education Level",
                options=[e.value for e in EducationLevel],
                help="Audience's highest education level.",
                label_visibility="collapsed"
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Psychographics row
        col_lifestyle, col_painpoints, col_aspirations = st.columns(3, gap="large")

        with col_lifestyle:
            lifestyle = dynamic_list_input(
                label="🏃‍♀️ Lifestyle Keywords",
                key="lifestyle_list",
                default_value=["gym", "healthy eating", "diet"]
            )

        with col_painpoints:
            pain_points = dynamic_list_input(
                label="😤 Pain Points",
                key="pain_points_list",
                default_value=["See a photo of a dish in social media but do not have the recipe"]
            )

        with col_aspirations:
            aspiration = dynamic_list_input(
                label="✨ Aspirations",
                key="aspirations_list",
                default_value=[""]
            )

    # Info box for audience section
    st.markdown("""
    <div class="info-box">
        <span class="info-box-icon">🎯</span>
        <strong>Audience Insights:</strong> The more specific you are about your audience's lifestyle, pain points, and aspirations, the more targeted and effective your ad script will be.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Generate Button Section
    st.markdown("""
    <div class="section-card" style="text-align: center; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);">
        <h3 style="color: #1e293b; margin-bottom: 1rem;">🚀 Ready to Generate Your Ad Script?</h3>
        <p style="color: #64748b; margin-bottom: 2rem;">Our AI agents will analyze your inputs and create a professional ad script optimized for your platform and audience.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Start Ad Script Generation!", type="primary", use_container_width=True):
        # Validation function
        def validate_inputs():
            errors = []
            if not product_name.strip():
                errors.append("Product name is required")
            if not product_description.strip():
                errors.append("Product description is required")
            if not product_features_dict:
                errors.append("At least one product feature is required")
            if not unique_selling_point or not any(usp.strip() for usp in unique_selling_point):
                errors.append("At least one unique selling point is required")
            if not problems_solved or not any(prob.strip() for prob in problems_solved):
                errors.append("At least one problem solved is required")
            if not lifestyle or not any(life.strip() for life in lifestyle):
                errors.append("At least one lifestyle item is required")
            if not pain_points or not any(pain.strip() for pain in pain_points):
                errors.append("At least one pain point is required")
            if not location:
                errors.append("At least one location must be selected")
            if not supported_platforms:
                errors.append("At least one supported platform must be selected")

            return errors

        # Validate inputs
        validation_errors = validate_inputs()

        if validation_errors:
            st.error("🚨 Please fix the following errors before continuing:")
            for error in validation_errors:
                st.write(f"• {error}")
        else:
            try:
                with st.spinner("🔄 Preparing your campaign data..."):
                    # Create the Product object
                    product = Product(
                        product_name=product_name,
                        product_description=product_description,
                        product_features=product_features_dict,
                        supported_platforms=[SupportedPlatform(p) for p in supported_platforms],
                        unique_selling_point=[usp for usp in unique_selling_point if usp.strip()],
                        problems_solved=[prob for prob in problems_solved if prob.strip()]
                    )

                    # Create the AudiencePersona object
                    audience_persona = AudiencePersona(
                        age_range=age_range,
                        gender=Gender(gender),
                        location=[Countries(c) for c in location],
                        income_range=IncomeRange(income_range),
                        education_level=EducationLevel(education_level) if education_level != "none" else None,
                        lifestyle=[life for life in lifestyle if life.strip()],
                        pain_points=[pain for pain in pain_points if pain.strip()],
                        aspiration=[asp for asp in aspiration if asp.strip()] if aspiration and any(
                            aspiration) else None
                    )

                    # Create the complete AgentState object
                    agent_state = AgentState(
                        campaign_goal=CampaignGoal(campaign_goal),
                        ad_platform=AdPlatform(ad_platform),
                        product=product,
                        product_feature_focus=product_feature_focus,
                        audience_persona=audience_persona,
                        creative_direction=CreativeDirection(creative_direction),
                        script_tone=ScriptTone(script_tone),
                        timestamp=datetime.now()
                    )

                    # Store in session state
                    st.session_state['agent_state'] = agent_state
                    st.session_state['workflow_status'] = 'ready'

                st.success("✅ Campaign configured successfully! Redirecting to AI processing...")

                # Navigate to processing page
                st.switch_page("pages/processing.py")

            except Exception as e:
                st.error(f"❌ Error creating workflow state: {str(e)}")
                with st.expander("🔍 View detailed error"):
                    st.code(traceback.format_exc())


if __name__ == "__main__":
    initial_input_ui()
