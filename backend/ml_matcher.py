from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def tfidf_match_score(resume_text: str, job_text: str) -> float:
    """Calculate match score using TF-IDF + Cosine Similarity"""
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform([resume_text, job_text])
        score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(float(score) * 100, 2)
    except Exception as e:
        return 0.0

def semantic_match_score(resume_skills: list, job_skills: list) -> float:
    """Calculate match score using Jaccard Similarity of skills"""
    if not job_skills:
        return 0.0
        
    resume_set = set([s.lower() for s in resume_skills])
    job_set = set([s.lower() for s in job_skills])
    
    intersection = resume_set.intersection(job_set)
    union = resume_set.union(job_set)
    
    if not union:
        return 0.0
        
    score = len(intersection) / len(union)
    return round(float(score) * 100, 2)

def get_missing_skills(resume_skills: list, job_skills: list) -> list:
    """Find skills in job description that are missing from resume"""
    resume_set = set([s.lower() for s in resume_skills])
    job_set = set([s.lower() for s in job_skills])
    missing = job_set - resume_set
    return list(missing)

def get_matching_skills(resume_skills: list, job_skills: list) -> list:
    """Find skills that match between resume and job"""
    resume_set = set([s.lower() for s in resume_skills])
    job_set = set([s.lower() for s in job_skills])
    matching = resume_set & job_set
    return list(matching)

def calculate_final_score(tfidf_score: float, semantic_score: float) -> float:
    """Combine TF-IDF and semantic scores with weights"""
    # 40% TF-IDF + 60% Semantic
    final = (0.4 * tfidf_score) + (0.6 * semantic_score)
    return round(final, 2)

def match_resume_to_job(
    resume_text: str,
    job_text: str,
    resume_skills: list,
    job_skills: list
) -> dict:
    """Main function — full matching analysis"""
    tfidf_score = tfidf_match_score(resume_text, job_text)
    semantic_score = semantic_match_score(resume_skills, job_skills)
    final_score = calculate_final_score(tfidf_score, semantic_score)

    return {
        "tfidf_score": tfidf_score,
        "semantic_score": semantic_score,
        "final_score": final_score,
        "matching_skills": get_matching_skills(resume_skills, job_skills),
        "missing_skills": get_missing_skills(resume_skills, job_skills),
        "verdict": (
            "Excellent Match! 🎉" if final_score >= 75 else
            "Good Match! 👍" if final_score >= 50 else
            "Partial Match 😐" if final_score >= 30 else
            "Low Match ❌"
        )
    }