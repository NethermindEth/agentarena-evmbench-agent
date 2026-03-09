"""
Core service for auditing Solidity contracts using OpenAI.
"""
import json
import logging
from typing import List
from pydantic import BaseModel, Field
from openai import OpenAI

from agent.services.prompts.audit_prompt import AUDIT_PROMPT

logger = logging.getLogger(__name__)

class VulnerabilityFinding(BaseModel):
    """Model representing a single vulnerability finding."""
    title: str = Field(..., description="Title of the vulnerability")
    description: str = Field(..., description="Detailed description of the vulnerability")
    severity: str = Field(..., description="Severity level: Critical, High, Medium, Low, or Informational")
    file_paths: List[str] = Field(..., description="List of file paths containing the vulnerability")

class Audit(BaseModel):
    """Model representing the complete audit response."""
    findings: List[VulnerabilityFinding] = Field(default_factory=list, description="List of vulnerability findings")
