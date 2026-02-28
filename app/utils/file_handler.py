"""File handling utilities."""

import os
import uuid
import tempfile
from typing import Optional
from pathlib import Path
import aiofiles
from fastapi import UploadFile
import pdfplumber

from app.config import settings


class FileHandler:
    """Handle file uploads and processing."""
    
    @staticmethod
    async def save_upload_file(upload_file: UploadFile) -> str:
        """Save uploaded file to temporary location."""
        # Create temp directory if it doesn't exist
        Path(settings.TEMP_DIR).mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        file_extension = Path(upload_file.filename).suffix
        temp_file_path = os.path.join(
            settings.TEMP_DIR,
            f"{uuid.uuid4()}{file_extension}"
        )
        
        # Save file
        async with aiofiles.open(temp_file_path, 'wb') as f:
            content = await upload_file.read()
            await f.write(content)
        
        return temp_file_path
    
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        """Extract text from PDF file."""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")
        finally:
            # Clean up temporary file
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
        
        return text.strip()
    
    @staticmethod
    def validate_file_size(file_size: int) -> bool:
        """Validate file size."""
        return file_size <= settings.MAX_FILE_SIZE
    
    @staticmethod
    def validate_file_extension(filename: str) -> bool:
        """Validate file extension."""
        file_extension = Path(filename).suffix.lower()
        return file_extension in settings.ALLOWED_EXTENSIONS
