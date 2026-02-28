from pydantic import BaseModel
from typing import List, Optional, Dict
from enum import Enum


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"

class SkillMatch(BaseModel):
    skill: str
    found_in_github: bool
    confidence: float
    github_projects: List[str]


class VerificationResponse(BaseModel):
    timestamp: str
    resume_skills: List[str]
    github_skills: List[str]
    matched_skills: List[SkillMatch]
    total_resume_skills: int
    total_github_skills: int
    matched_count: int
    match_percentage: float
    trust_score: float
    risk_level: str
    recommendations: List[str]
    github_stats: Dict


class ErrorResponse(BaseModel):
    error: str
    message: str