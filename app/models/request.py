"""Request models for API endpoints."""

from typing import Optional
from pydantic import BaseModel, Field, validator
from fastapi import UploadFile


class VerificationRequest(BaseModel):
    """Resume verification request model."""
    
    github_username: str = Field(
        ..., 
        min_length=1,
        max_length=39,
        description="GitHub username for verification"
    )
    
    @validator('github_username')
    def validate_github_username(cls, v):
        """Validate GitHub username format."""
        import re
        if not re.match(r'^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38}$', v):
            raise ValueError('Invalid GitHub username format')
        return v


class SkillExtractionRequest(BaseModel):
    """Skill extraction request model."""
    
    text: str = Field(
        ...,
        min_length=100,
        description="Resume text for skill extraction"
    )
