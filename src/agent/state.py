"""
Defines Pydantic models and enumerations for representing campaign, product, audience, and workflow state within the
ad campaign generation system.

Author: Peyman Kh
Last Edit: 27-07-2025
"""
# Import libraries
import json
from enum import Enum
from datetime import datetime
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field, field_validator


class CampaignGoal(str, Enum):
    """
    Enumeration of possible objectives for an advertising campaign.
    """
    awareness = 'awareness'
    traffic = 'traffic'
    engagement = 'engagement'
    leads = 'leads'
    app_installs = 'app_installs'


class AdPlatform(str, Enum):
    """
    Enumeration of specific ad placements across different social platforms.
    """
    instagram_reels = 'instagram_reels'
    instagram_stories = 'instagram_stories'
    instagram_feeds = 'instagram_feeds'
    facebook_feeds = 'facebook_feeds'
    facebook_stories = 'facebook_stories'
    youtube_shorts = 'youtube_shorts'
    tiktok_feed = 'tiktok_feed'
    snapchat_spotlight = 'snapchat_spotlight'


class SupportedPlatform(str, Enum):
    """
    Mobile platforms supported by the product.
    """
    ios = "ios"
    android = "android"
    web="web"


class Product(BaseModel):
    """
    Details about the app being advertised.
    """
    product_name: str = Field(
        ..., description="name of the app."
    )
    product_description: str = Field(
        ..., description="A brief overview of the app."
    )
    product_features: Dict[str, str] = Field(
        ..., description="Dictionary mapping feature names to descriptions."
    )
    supported_platforms: List[SupportedPlatform] = Field(
        description="Supported platforms for the application.",
        default_factory=lambda: [SupportedPlatform.ios]
    )
    unique_selling_point: List[str] = Field(
        ..., description="List of unique selling points for the product."
    )
    problems_solved: List[str] = Field(
        ..., description="List of problems solved by the product."
    )


class Gender(str, Enum):
    """
    Gender identity options for the target audience.
    """
    male = "male"
    female = "female"
    all = "all"


class Countries(str, Enum):
    """
    Enumeration of supported audience countries.
    """
    usa = "usa"
    uk = "uk"
    canada = "canada"
    australia = "australia"


class IncomeRange(str, Enum):
    """
    Income range categories for audience segmentation.
    """
    low = "<$30k"
    lower_middle = "$30k–$60k"
    middle = "$60k–$100k"
    upper_middle = "$100k–$200k"
    high = ">$200k"


class EducationLevel(str, Enum):
    """
    Highest educational attainment of an audience segment.
    """
    none = "none"
    high_school = "high_school"
    some_college = "some_college"
    bachelors = "bachelors"
    masters = "masters"
    doctorate = "doctorate"


class AudiencePersona(BaseModel):
    """
    Structured profile representing characteristics of the target audience.
    """
    age_range: str = Field(
        ..., description="Age range of the target audience."
    )
    gender: Gender = Field(
        ..., description="Gender of the target audience."
    )
    location: List[Countries] = Field(
        ..., description="List of target audience countries."
    )
    income_range: IncomeRange = Field(
        ..., description="Income range category of the target audience."
    )
    education_level: Optional[EducationLevel] = Field(
        default=None,
        description="Education level of the target audience."
    )
    lifestyle: List[str] = Field(
        ..., description="Lifestyle characteristics of the target audience."
    )
    pain_points: List[str] = Field(
        ..., description="Key pain points and challenges faced by the audience."
    )
    aspiration: Optional[List[str]] =  Field(
        default=None,
        description="What the audience wants to achieve."
    )


class CreativeDirection(str, Enum):
    """
    Enumeration of common creative approaches for ad messaging angles.
    """
    user_generated_content = "user_generated_content"
    problem_solution = "problem_solution"
    testimonial = "testimonial"
    lifestyle = "lifestyle"
    educational = "educational"
    motivational = "motivational"
    product_in_action = "product_in_action"
    gamification = "gamification"
    humor = "humor"
    storytelling = "storytelling"
    day_in_life = "day_in_life"


class ScriptTone(str, Enum):
    """
    Enumeration of tones that can be applied to scriptwriting for effective and engaging ad content.
    """
    friendly = "friendly"                   # Warm, approachable, and welcoming
    conversational = "conversational"       # Casual and natural, like a personal chat
    authoritative = "authoritative"         # Demonstrates expertise and confidence
    energetic = "energetic"                 # Brisk, dynamic, and high-spirited
    enthusiastic = "enthusiastic"           # Expresses excitement and positive energy
    humorous = "humorous"                   # Uses wit or light-heartedness for engagement
    emotional = "emotional"                 # Appeals to feelings (joy, empathy, etc.)
    inspirational = "inspirational"         # Uplifts and motivates with positive messaging
    motivational = "motivational"           # Drives action through encouragement
    trustworthy = "trustworthy"             # Sincere, credible, and reliable
    sincere = "sincere"                     # Honest, heartfelt, and authentic
    playful = "playful"                     # Fun, lively, and sometimes mischievous
    urgent = "urgent"                       # Conveys time-sensitivity to prompt quick response
    dramatic = "dramatic"                   # Uses suspense or intensity for impact
    sophisticated = "sophisticated"         # Polished, refined, and elegant
    professional = "professional"           # Formal, respectful, and businesslike
    calm = "calm"                           # Gentle, relaxed, and reassuring
    bold = "bold"                           # Daring and attention-grabbing
    clever = "clever"                       # Smart, witty, and inventive in messaging
    reassuring = "reassuring"               # Offers comfort and confidence in the product/brand


class AudienceInsight(BaseModel):
    """
    structured psychographic and behavioral details of user persona
    """
    # Interests & Hobbies (Psychographic)
    common_interests: List[str] = Field(
        ...,
        description="A list of 3 common hobbies, interests, and passions that are plausible for this audience segment. Be specific (e.g., 'sustainable living', 'DIY home improvement', 'online gaming communities')."
    )

    # Media Consumption Habits (Behavioral)
    media_consumption_habits: List[str] = Field(
        ...,
        description="3 key ways this audience consumes media, including types of content and platforms (e.g., 'spends hours on TikTok watching short-form educational content', 'prefers in-depth articles on tech blogs', 'listens to podcasts during commute')."
    )

    # Lifestyle & Daily Routine (Psychographic/Behavioral)
    typical_daily_routine_snippets: List[str] = Field(
        ...,
        description="3 brief descriptions of typical daily activities or scenarios that define their lifestyle (e.g., 'commutes to work in a busy city', 'manages household and childcare', 'works remotely from home')."
    )

    # Core Values & Beliefs (Psychographic)
    core_values_and_beliefs: List[str] = Field(
        ...,
        description="3 fundamental values or beliefs that likely influence their decisions and worldview (e.g., 'values financial stability and security', 'prioritizes environmental sustainability', 'believes in continuous self-improvement')."
    )

    # Purchasing Behavior & Decision-Making (Behavioral)
    decision_making_factors: List[str] = Field(
        ...,
        description="3 key factors that influence their purchase decisions for products like yours (e.g., 'influenced by peer reviews and recommendations', 'seeks value for money', 'prioritizes convenience and time-saving', 'brand loyalty is important')."
    )

    # Preferred Content Formats & Tone (Behavioral)
    preferred_content_formats_and_tone: List[str] = Field(
        ...,
        description="3 types of content and tones they respond best to in advertising (e.g., 'short, engaging video tutorials', 'authentic user-generated content', 'informative infographics with a professional tone')."
    )

    # Elaborated Pain Points & Desired Outcomes (Psychographic/Motivational)
    elaborated_pain_points: List[str] = Field(
        ...,
        description="3 more detailed, scenario-based descriptions of their key challenges and frustrations related to the problem your product solves."
    )
    elaborated_aspiration_outcomes: List[str] = Field(
        ...,
        description="3 specific and vivid descriptions of what they want to achieve, how they envision success, and the emotional benefit."
    )

    # Brand Perception & Trust (Psychographic/Behavioral)
    how_they_perceive_brands_like_yours: List[str] = Field(
        ...,
        description="3 insights into how this audience typically views or interacts with brands in your product category (e.g., 'skeptical of exaggerated claims', 'expects excellent customer service', 'looks for social proof')."
    )

    # Unique or Niche Characteristics (Psychographic)
    unique_or_niche_insights: List[str] = Field(
        ...,
        description="2 other unique, non-obvious, or niche insights that stand out for this specific audience profile that might influence ad strategy. This is where the LLM can really shine."
    )


class Scene(BaseModel):
    """
    Represents a single scene in a video ad script.
    """
    scene_number: int = Field(..., description="Sequential number of the scene.")
    visual_description: str = Field(..., description="Detailed description of what should be shown on screen.")
    audio_description: str = Field(..., description="Description of background music, sound effects, or ambient noise.")
    on_screen_text: Optional[str] = Field(None, description="Text overlays that appear on screen during this scene.")
    voiceover_dialogue: Optional[str] = Field(None, description="Dialogue spoken by a voiceover artist or character in this scene.")
    duration_seconds: float = Field(..., description="Approximate duration of the scene in seconds.")


class VideoScriptDraft(BaseModel):
    """
    Structured representation of a video ad script.
    """
    script_type: str = Field("Video", description="Type of script (e.g., 'Video').")
    ad_platform_target: str = Field(..., description="The specific ad platform this script is optimized for.")
    duration_estimate_seconds: float = Field(..., description="Estimated total duration of the script in seconds.")
    scenes: List[Scene] = Field(
        default_factory=list,
        description="A list of structured scenes for the video ad."
    )
    call_to_action_text: str = Field(..., description="The main call to action text to be used.")
    suggested_hashtags: List[str] = Field(
        default_factory=list,
        description="Relevant hashtags to include with the ad post."
    )
    key_takeaway: str = Field(..., description="A concise sentence summarizing the ad's main point.")


class StaticAdDraft(BaseModel):
    """
    Structured representation of a static (image/feed) ad script.
    """
    script_type: str = Field("Static", description="Type of script (e.g., 'Static').")
    ad_platform_target: str = Field(..., description="The specific ad platform this script is optimized for.")
    headline: str = Field(..., description="The headline or primary title of the ad copy.")
    body_copy: str = Field(..., description="The main body text of the ad copy.")
    image_description: str = Field(..., description="A detailed description of the ad's main visual.")
    on_image_text: str = Field(..., description="Test on the image")
    call_to_action_text: str = Field(..., description="The main call to action text to be used.")
    suggested_hashtags: List[str] = Field(
        default_factory=list,
        description="Relevant hashtags to include with the ad post."
    )
    key_takeaway: str = Field(..., description="A concise sentence summarizing the ad's main point.")


ScriptDraft = Union[VideoScriptDraft, StaticAdDraft]


class EvaluationCriterion(str, Enum):
    """
    Specific criteria used to evaluate an ad script.
    """
    hook = "hook"
    clarity = "clarity"
    conciseness = "conciseness"
    emotional_appeal = "emotional_appeal"
    call_to_action_strength = "call_to_action_strength"
    brand_voice_adherence = "brand_voice_adherence"
    platform_compliance = "platform_compliance"
    relevance_to_audience = "relevance_to_audience"
    feature_highlight_effectiveness = "feature_highlight_effectiveness"
    uniqueness_originality = "uniqueness_originality"
    overall_impact = "overall_impact"


class EvaluationMetric(BaseModel):
    """
    Represents a single evaluation metric score.
    """
    score: int = Field(..., ge=1, le=5, description="Score for the criterion (1=Poor, 5=Excellent).")
    feedback: str = Field(..., description="Specific, constructive feedback for this criterion.")


class EvaluationReport(BaseModel):
    """
    Comprehensive report on the evaluation of an ad script, detailing scores and feedback per criterion.
    """
    overall_score: float = Field(..., ge=1, le=5, description="Overall aggregated score for the script (1=Poor, 5=Excellent).")
    detailed_scores: Dict[EvaluationCriterion, EvaluationMetric] = Field(
        ..., description="Dictionary mapping each evaluation criterion to its score and specific feedback."
    )
    summary_feedback: str = Field(
        ..., description="Concise summary of the script's strengths and areas for improvement."
    )
    actionable_recommendations: List[str] = Field(
        ..., description="Specific recommendation (e.g., 'Revise CTA', 'Shorten script', 'Proceed to variations')."
    )
    is_approved_for_next_stage: bool = Field(
        ..., description="Indicates if the script meets quality thresholds to proceed (e.g., to human review or variation generation)."
    )


class VariationRequest(BaseModel):
    """
    Request for generating a single A/B test variation with specific changes.
    """
    variation_focus: str = Field(
        ...,
        description="The primary focus of this variation (e.g., 'Hook + CTA + Emotional Tone')"
    )
    target_changes: List[str] = Field(
        ...,
        description="Specific changes to make: hook modification, CTA enhancement, emotional tone shift"
    )


class SingleVariation(BaseModel):
    """
    Represents a single, refined A/B test variation.
    """
    variation_name: str = Field(..., description="Name/identifier for this variation")
    variation_type: str = Field(..., description="Type of variation (e.g., 'Enhanced Hook + CTA + Tone')")
    base_script_comparison: str = Field(..., description="Brief comparison with the base script")
    ad_script_variation: ScriptDraft = Field(..., description="The refined variation script")
    variation_evaluation_report: Optional[EvaluationReport] = Field(
        default=None, description="Final evaluation report for this variation"
    )
    variation_iteration_count: int = Field(default=0, description="Number of refinement iterations")
    notes: Optional[str] = Field(None, description="Additional notes about this variation")


class AgentState(BaseModel):
    """
    Core state object passed between workflow nodes, capturing key context for campaign generation.
    """
    campaign_goal: CampaignGoal = Field(
        ..., description="Main goal of the ad campaign."
    )
    ad_platform: AdPlatform = Field(
        ..., description="Advertising platform to be used."
    )
    product: Product = Field(
        ..., description="Details about the product being advertised."
    )
    product_feature_focus: str = Field(
        ..., description="Which feature should the ad focus on?"
    )
    audience_persona: AudiencePersona = Field(
        ..., description="Detailed profile of the intended target audience"
    )
    creative_direction: CreativeDirection = Field(
        ..., description="messaging angle of the ad."
    )
    script_tone: ScriptTone = Field(
        ...,
        description="Requested brand voice or tone for the ad script."
    )
    # Workflow fields
    audience_insight: Optional[AudienceInsight] = Field(
        default=None,
        description="Psychographic and behavioral details of user persona."
    )
    brainstormed_hooks: Optional[List[str]] = Field(
        default=None,
        description="List of brainstormed hook ideas or attention-grabbing opening lines for the script."
    )
    generated_ctas: Optional[List[str]] = Field(
        default=None,
        description="List of generated call-to-action phrases for use in the ad script."
    )
    core_message_pillars: Optional[List[str]] = Field(
        default=None,
        description="3 most important messages the ad should convey."
    )
    emotional_triggers: Optional[List[str]] = Field(
        default=None,
        description="Specific emotions to evoke in the audience."
    )
    primary_visual_concept: str = Field(
        default=None,
        description="A brief description of the recommended visual style and concepts for the ad."
    )
    audio_strategy: str = Field(
        default=None,
        description="A brief description of the recommended audio strategy (e.g., trending music, voiceover)."
    )
    script_draft: Optional[ScriptDraft] = Field(
        default=None,
        description="Current working draft of the ad script, generated or updated during the workflow."
    )
    evaluation_report: Optional[EvaluationReport] = Field(
        default=None,
        description="Detailed multi-criteria report from the Evaluator Agent assessing the current script draft."
    )
    revision_feedback: Optional[str] = Field(
        default=None,
        description="Evaluator or reviewer feedback with specific revision requests for the scriptwriter."
    )
    variation_request: Optional[VariationRequest] = Field(
        default=None,
        description="Request details for generating a single variation"
    )
    variation_script_draft: Optional[ScriptDraft] = Field(
        default=None,
        description="Current working draft of the variation script"
    )
    variation_evaluation_report: Optional[EvaluationReport] = Field(
        default=None,
        description="Evaluation report for the variation script"
    )
    variation_iteration_count: int = Field(
        default=0,
        description="Number of refinement iterations for the variation"
    )
    single_variation_result: Optional[SingleVariation] = Field(
        default=None,
        description="Final single variation result with all refinements"
    )
    is_variation_workflow: bool = Field(
        default=False,
        description="Flag to indicate if this is a variation generation workflow"
    )
    tool_calls_history: Optional[List[Dict]] = Field(
        default=None,
        description="Chronological log of tool or agent calls invoked during the workflow, with relevant inputs/outputs."
    )
    script_iteration_history: Optional[List[Dict]] = Field(
        default=None,
        description="History of script refinement iterations, including previous evaluation reports and refined scripts."
    )
    iteration_count: int = Field(
        default=0,
        description="Number of refinement iterations the script has gone through."
    )
    total_llm_tokens: int = Field(
        default=0,
        description="Total number of LLM tokens (input + output) used across all calls."
    )
    timestamp: Optional[datetime] = Field(
        default=None,
        description="Timestamp indicating when this AgentState was last updated or processed."
    )
    human_review_decision: Optional[str] = Field(
        default=None,
        description="Decision made by human reviewer: 'approved', 'minor_revision', or 'major_rework'."
    )
