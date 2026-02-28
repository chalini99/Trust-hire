"""API endpoints for the Resume Verification System."""

from typing import Optional
from urllib import response
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse

from app.models.request import VerificationRequest
from app.models.response import VerificationResponse, ErrorResponse, SkillMatch
from app.services.resume_parser import ResumeParser
from app.services.skill_extractor import SkillExtractor
from app.services.github_verifier import GitHubVerifier
from app.services.scoring_engine import ScoringEngine
from app.utils.file_handler import FileHandler
from app.config import settings
from datetime import datetime


router = APIRouter()
resume_parser = ResumeParser()
skill_extractor = SkillExtractor()
github_verifier = GitHubVerifier()
scoring_engine = ScoringEngine()
file_handler = FileHandler()


@router.post("/verify", response_model=VerificationResponse)
async def verify_resume(
    resume: UploadFile = File(...),
    github_username: str = Form(...)
):
    """
    Complete resume verification endpoint.
    
    - Upload PDF resume
    - Extract skills from resume
    - Verify against GitHub profile
    - Return trust score and risk assessment
    """
    try:
        # Validate file
        if not file_handler.validate_file_extension(resume.filename):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed"
            )
        
        if not file_handler.validate_file_size(resume.size):
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds {settings.MAX_FILE_SIZE / 1024 / 1024}MB limit"
            )
        
        # Save and parse resume
        pdf_path = await file_handler.save_upload_file(resume)
        resume_data = await resume_parser.parse_pdf(pdf_path)
        
        # Extract skills from resume
        resume_skills = skill_extractor.extract_skills(resume_data['text'])
        
        if not resume_skills:
            raise HTTPException(
                status_code=400,
                detail="No technical skills found in resume"
            )
        
        # Verify GitHub profile
        github_data = await github_verifier.verify_user(github_username)
        github_skills = github_data['skills']
        
        # Calculate match score
        matched_skills, match_percentage = scoring_engine.calculate_match_score(
            resume_skills,
            github_skills
        )
        
        # Calculate trust score
        trust_score = scoring_engine.calculate_trust_score(
            match_percentage,
            github_data['stats'],
            len(resume_skills),
            len(github_skills)
        )
        
        # Determine risk level
        risk_level = scoring_engine.determine_risk_level(trust_score, match_percentage)
        
        # Generate recommendations
        unmatched_skills = [
            skill for skill in resume_skills
            if not any(m['found_in_github'] for m in matched_skills if m['skill'] == skill)
        ]
        recommendations = scoring_engine.generate_recommendations(
            trust_score,
            match_percentage,
            github_data['stats'],
            unmatched_skills
        )
        # Prepare github stats dictionary
        github_stats = github_data['stats']
        # Prepare response
       

# Prepare response
        return VerificationResponse(
    timestamp=datetime.utcnow().isoformat(),
    resume_skills=resume_skills,
    github_skills=github_skills,
    matched_skills=matched_skills,
    total_resume_skills=len(resume_skills),
    total_github_skills=len(github_skills),
    matched_count=len(matched_skills),
    match_percentage=match_percentage,
    trust_score=trust_score,
    risk_level=risk_level,
    recommendations=recommendations,
    github_stats=github_stats
)  
       
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Verification failed: {str(e)}"
        )


@router.post("/extract-skills")
async def extract_skills_only(resume: UploadFile = File(...)):
    """
    Extract skills from resume only.
    
    - Upload PDF resume
    - Extract and return technical skills
    """
    try:
        # Validate file
        if not file_handler.validate_file_extension(resume.filename):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed"
            )
        
        # Save and parse resume
        pdf_path = await file_handler.save_upload_file(resume)
        resume_data = await resume_parser.parse_pdf(pdf_path)
        
        # Extract skills
        skills = skill_extractor.extract_skills(resume_data['text'])
        ranked_skills = skill_extractor.rank_skills(skills, resume_data['text'])
        
        return {
            "skills": skills,
            "ranked_skills": [
                {"skill": skill, "frequency": count}
                for skill, count in ranked_skills
            ],
            "total_skills": len(skills),
            "word_count": resume_data['word_count']
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Skill extraction failed: {str(e)}"
        )


@router.get("/github-profile/{username}")
async def get_github_profile(username: str):
    """
    Get GitHub profile analysis.
    
    - Fetch GitHub user data
    - Extract skills and languages
    - Return profile statistics
    """
    try:
        github_data = await github_verifier.verify_user(username)
        return github_data
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"GitHub profile fetch failed: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION
    }
@router.post("/interview-questions")
async def generate_questions(skills: list[str]):
    questions = []

    for skill in skills:
        questions.append(f"What are the key concepts of {skill}?")
        questions.append(f"Explain a real-world project using {skill}.")

    return {"questions": questions}