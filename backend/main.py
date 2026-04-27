from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import tempfile

from pdf_parser import parse_resume
from nlp_extractor import analyze_resume, extract_skills
from ml_matcher import match_resume_to_job
from gemini_advisor import get_career_advice, get_skill_resources

app = FastAPI(title="Resume Screener API")

# Allow React frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Resume Screener API is running!"}

@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    job_title: str = Form("")
):
    """Main endpoint — upload resume + job description → get full analysis"""

    # Save uploaded PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(resume.file, tmp)
        tmp_path = tmp.name

    try:
        # Step 1 — Parse PDF
        parsed = parse_resume(tmp_path)
        resume_text = parsed["cleaned_text"]

        # Step 2 — NLP Analysis
        resume_analysis = analyze_resume(resume_text)
        resume_skills = resume_analysis["skills"]

        # Step 3 — Extract job skills
        job_skills = extract_skills(job_description)

        # Step 4 — ML Matching
        match_result = match_resume_to_job(
            resume_text,
            job_description,
            resume_skills,
            job_skills
        )

        # Step 5 — Gemini AI Advice
        advice = get_career_advice(
            resume_skills=resume_skills,
            missing_skills=match_result["missing_skills"],
            matching_skills=match_result["matching_skills"],
            final_score=match_result["final_score"],
            job_title=job_title
        )

        return {
            "success": True,
            "resume_info": {
                "word_count": parsed["word_count"],
                "email": resume_analysis["email"],
                "phone": resume_analysis["phone"],
                "education": resume_analysis["education"],
                "skills": resume_skills,
                "entities": resume_analysis["entities"]
            },
            "job_info": {
                "skills_required": job_skills
            },
            "match_result": match_result,
            "ai_advice": advice
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

    finally:
        # Clean up temp file
        os.unlink(tmp_path)

@app.get("/skill-resources/{skill}")
async def skill_resources(skill: str):
    """Get learning resources for a specific skill"""
    result = get_skill_resources(skill)
    return result

@app.get("/health")
def health():
    return {"status": "healthy"}

import os
import uvicorn
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)