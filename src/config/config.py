"""
This module is settings for the project. It securely loads environment variables
and validate the presence of the necessary API keys.
"""
from enum import Enum
from pathlib import Path
from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings


class LogLevel(str, Enum):
    """Allowed log levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LangChainConfig(BaseSettings):
    """
    LangChain Backend Server Configuration

    This configuration supports multiple LLM providers, vector stores,
    and deployment environments with GCP Secret Manager integration.
    """

    # APPLICATION SETTINGS
    app_name: str = Field(description="Application name")
    app_version: str = Field(description="Application version")
    environment: str = Field(description="Environment (development/staging/production)")
    debug: bool = Field(description="Enable debug mode")

    # Server configuration - MADE MANDATORY
    host: str = Field(description="Server host")
    port: int = Field(ge=1, le=65535, description="Server port")

    # Logging
    log_level: LogLevel = Field(description="Logging level")
    log_format: str = Field(description="Log format")

    # Node1: Audience Insight
    audience_insight_llm: str = Field(description="LLM name for audience insight node")
    audience_insight_api_key: str = Field(description="API key audience insight LLM")
    audience_insight_temperature: str = Field(description="Temperature for audience insight node")

    # Node2: Creative Strategy
    creative_strategy_llm: str = Field(description="LLM name for creative strategy node")
    creative_strategy_api_key: str = Field(description="API key creative strategy LLM")
    creative_strategy_temperature: str = Field(description="Temperature for creative strategy node")

    # Node3: Script Generation
    script_generation_llm1: str = Field(description="LLM name for script generation node")
    script_generation_api_key1: str = Field(description="API key script generation LLM")
    script_generation_temperature1: str = Field(description="Temperature for script generation node")

    script_generation_llm2: str = Field(description="LLM name for script generation node")
    script_generation_api_key2: str = Field(description="API key script generation LLM")
    script_generation_temperature2: str = Field(description="Temperature for script generation node")

    # Node4: Script Evaluation
    script_evaluation_and_refinement_llm: str = Field(description="LLM name for script evaluation node")
    script_evaluation_and_refinement_api_key: str = Field(description="API key script evaluation LLM")
    script_evaluation_and_refinement_temperature: str = Field(description="Temperature for script evaluation node")


    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment.lower() == "production"

    class Config:
        env_file = Path(__file__).parent.parent.parent / '.env'
        env_file_encoding = 'utf-8'

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            return (env_settings,)


# Initialize configuration with validation
try:
    config = LangChainConfig()

except Exception as e:
    raise


# Export config instance
__all__ = ['config', 'LangChainConfig']
