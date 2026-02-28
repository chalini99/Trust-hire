"""Skill extraction service using NLP and keyword matching."""

import re
from typing import List, Set
from collections import Counter
from app.utils.skill_database import SkillDatabase


class SkillExtractor:
    """Extract skills from resume text."""
    
    def __init__(self):
        self.skill_db = SkillDatabase()
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text using keyword matching and NLP."""
        text_lower = text.lower()
        found_skills = set()
        
        # Get all known skills
        all_skills = self.skill_db.get_all_skills()
        
        # Method 1: Direct keyword matching
        for skill in all_skills:
            # Create word boundary pattern for accurate matching
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill)
        
        # Method 2: Extract from common skill patterns
        skill_patterns = [
            r'(?i)proficient in (.+?)(?:\.|,|\n|$)',
            r'(?i)experience with (.+?)(?:\.|,|\n|$)',
            r'(?i)skilled in (.+?)(?:\.|,|\n|$)',
            r'(?i)knowledge of (.+?)(?:\.|,|\n|$)',
            r'(?i)familiar with (.+?)(?:\.|,|\n|$)',
            r'(?i)expertise in (.+?)(?:\.|,|\n|$)',
        ]
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                # Split by common delimiters
                potential_skills = re.split(r'[,;]|\band\b', match)
                for ps in potential_skills:
                    ps = ps.strip().lower()
                    # Check if it's a known skill
                    normalized = self.skill_db.normalize_skill(ps)
                    if normalized in all_skills:
                        found_skills.add(normalized)
        
        # Method 3: Look for programming language file extensions
        extension_mapping = {
            '.py': 'python',
            '.js': 'javascript',
            '.java': 'java',
            '.cpp': 'c++',
            '.cs': 'c#',
            '.rb': 'ruby',
            '.go': 'go',
            '.rs': 'rust',
            '.kt': 'kotlin',
            '.swift': 'swift',
            '.ts': 'typescript',
            '.php': 'php',
            '.r': 'r',
            '.scala': 'scala',
        }
        
        for ext, lang in extension_mapping.items():
            if ext in text_lower:
                found_skills.add(lang)
        
        # Remove duplicates and return sorted list
        return sorted(list(found_skills))
    
    def rank_skills(self, skills: List[str], text: str) -> List[tuple]:
        """Rank skills by frequency in text."""
        text_lower = text.lower()
        skill_counts = []
        
        for skill in skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            count = len(re.findall(pattern, text_lower))
            skill_counts.append((skill, count))
        
        # Sort by frequency
        skill_counts.sort(key=lambda x: x[1], reverse=True)
        return skill_counts
