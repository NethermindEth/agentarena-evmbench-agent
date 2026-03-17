"""
Configuration management for the AI agent.
"""

import os
from typing import Dict, Any, Optional, Literal
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    # Required fields for local mode
    api_key: str = Field(..., env="API_KEY")
    model: Literal[
        'codex-gpt-5.1-codex-max', 'codex-gpt-5.2', 'gpt-5.3-codex',
        'claude-opus-4-6', 'claude-sonnet-4-6',
        'gemini-3.1-pro-preview', 'gemini-3.1-flash-lite-preview'
    ] = Field("gpt-5.3-codex", env="MODEL")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_file: str = Field("agent.log", env="LOG_FILE")
    
    # EVMBench service URL
    evmbench_url: str = Field("http://localhost:1337", env="EVMBENCH_URL")

    # Additional fields for server mode
    agentarena_api_key: Optional[str] = Field(None, env="AGENTARENA_API_KEY")
    webhook_auth_token: Optional[str] = Field(None, env="WEBHOOK_AUTH_TOKEN")
    data_dir: Optional[str] = Field("./data", env="DATA_DIR")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

def load_config() -> Settings:
    """Load and return application configuration."""
    load_dotenv(override=True)
    return Settings() 