"""Configuration settings for the Resume Verification System."""

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    APP_NAME: str = "Resume Verification System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # GitHub API
    GITHUB_API_URL: str = "https://api.github.com"
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    
    # File Upload
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS: List[str] = [".pdf"]
    
    # Scoring Thresholds
    HIGH_MATCH_THRESHOLD: float = 0.7
    MEDIUM_MATCH_THRESHOLD: float = 0.4
    
    # Temporary file storage
    TEMP_DIR: str = "/tmp/resume_uploads"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
