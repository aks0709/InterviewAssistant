"""Simplified file parsing service for backend."""
import PyPDF2
from io import BytesIO

def parse_pdf(file_content: bytes) -> str:
    """Parse PDF file and extract text."""
    try:
        pdf_file = BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise ValueError(f"Error parsing PDF: {str(e)}")

def parse_file(file_content: bytes, filename: str) -> str:
    """Parse file based on extension."""
    filename_lower = filename.lower()
    
    if filename_lower.endswith('.pdf'):
        return parse_pdf(file_content)
    elif filename_lower.endswith('.txt'):
        return file_content.decode('utf-8')
    else:
        # For unsupported files, return filename as placeholder
        return f"File: {filename}\nPlease convert to PDF or TXT format."