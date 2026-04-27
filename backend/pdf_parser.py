import fitz  # PyMuPDF
import re
import os

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract raw text from a PDF file"""
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")
    return text.strip()

def clean_text(text: str) -> str:
    """Clean extracted text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s\.\,\@\+\-\/]', ' ', text)
    return text.strip()

def parse_resume(pdf_path: str) -> dict:
    """Main function — extract and clean text from resume PDF"""
    raw_text = extract_text_from_pdf(pdf_path)
    cleaned = clean_text(raw_text)
    
    return {
        "raw_text": raw_text,
        "cleaned_text": cleaned,
        "word_count": len(cleaned.split()),
        "char_count": len(cleaned)
    }