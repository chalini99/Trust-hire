"""Resume parsing service."""

import re
from typing import Dict, Any
from app.utils.file_handler import FileHandler


class ResumeParser:
    """Parse and extract information from resumes."""
    
    def __init__(self):
        self.file_handler = FileHandler()
    
    async def parse_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Parse PDF resume and extract text."""
        text = self.file_handler.extract_text_from_pdf(pdf_path)
        
        if not text or len(text) < 100:
            raise ValueError("Insufficient text extracted from resume")
        
        return {
            'text': text,
            'word_count': len(text.split()),
            'char_count': len(text)
        }
    
    def extract_sections(self, text: str) -> Dict[str, str]:
        """Extract different sections from resume text."""
        sections = {
            'skills': '',
            'experience': '',
            'education': '',
            'projects': ''
        }
        
        # Simple section detection based on keywords
        section_patterns = {
            'skills': r'(?i)(skills?|technical skills?|core competenc\w+|expertise)',
            'experience': r'(?i)(experience|work experience|employment|professional experience)',
            'education': r'(?i)(education|academic|qualification|degree)',
            'projects': r'(?i)(projects?|portfolio|work samples)'
        }
        
        lines = text.split('\n')
        current_section = None
        
        for line in lines:
            # Check if line matches any section header
            for section, pattern in section_patterns.items():
                if re.search(pattern, line):
                    current_section = section
                    break
            
            # Add line to current section
            if current_section:
                sections[current_section] += line + '\n'
        
        return sections
