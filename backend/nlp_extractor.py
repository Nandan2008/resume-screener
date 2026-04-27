import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Skills database
SKILLS_DB = [
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
    "react", "angular", "vue", "nodejs", "fastapi", "django", "flask",
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "scikit-learn", "keras",
    "sql", "mysql", "postgresql", "mongodb", "redis",
    "aws", "azure", "gcp", "docker", "kubernetes",
    "git", "linux", "rest api", "graphql",
    "data analysis", "pandas", "numpy", "matplotlib",
    "communication", "teamwork", "leadership", "problem solving"
]

def extract_skills(text: str) -> list:
    """Extract skills from text by matching against skills database"""
    text_lower = text.lower()
    found_skills = []
    for skill in SKILLS_DB:
        if skill in text_lower:
            found_skills.append(skill)
    return list(set(found_skills))

def extract_entities(text: str) -> dict:
    """Use spaCy to extract named entities"""
    doc = nlp(text)
    entities = {
        "organizations": [],
        "locations": [],
        "dates": []
    }
    for ent in doc.ents:
        if ent.label_ == "ORG":
            entities["organizations"].append(ent.text)
        elif ent.label_ == "GPE":
            entities["locations"].append(ent.text)
        elif ent.label_ == "DATE":
            entities["dates"].append(ent.text)
    return entities

def extract_email(text: str) -> str:
    """Extract email address"""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, text)
    return match.group() if match else ""

def extract_phone(text: str) -> str:
    """Extract phone number"""
    pattern = r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}'
    match = re.search(pattern, text)
    return match.group() if match else ""

def extract_education(text: str) -> list:
    """Extract education qualifications"""
    education_keywords = [
        "bachelor", "master", "phd", "b.tech", "m.tech", 
        "b.sc", "m.sc", "mba", "degree", "diploma"
    ]
    text_lower = text.lower()
    found = []
    for keyword in education_keywords:
        if keyword in text_lower:
            found.append(keyword.upper())
    return list(set(found))

def analyze_resume(text: str) -> dict:
    """Main function — full NLP analysis of resume"""
    return {
        "skills": extract_skills(text),
        "entities": extract_entities(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "education": extract_education(text)
    }