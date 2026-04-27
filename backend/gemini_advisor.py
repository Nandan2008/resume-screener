import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def get_career_advice(
    resume_skills: list,
    missing_skills: list,
    matching_skills: list,
    final_score: float,
    job_title: str = ""
) -> dict:
    """Get AI-powered career advice from Gemini"""

    prompt = f"""
    You are an expert career coach and HR specialist.
    
    Analyze this resume match data and provide actionable advice:
    
    Job Title: {job_title if job_title else "Not specified"}
    Match Score: {final_score}%
    Candidate's Current Skills: {', '.join(resume_skills)}
    Skills that Match the Job: {', '.join(matching_skills)}
    Missing Skills: {', '.join(missing_skills)}
    
    Please provide:
    1. Overall assessment (2-3 sentences)
    2. Top 3 skills to learn immediately with free resources
    3. How to improve the resume for this role
    4. Interview preparation tips for this role
    
    Be specific, practical and encouraging.
    Format your response clearly with these exact headings:
    ASSESSMENT:
    SKILLS TO LEARN:
    RESUME TIPS:
    INTERVIEW TIPS:
    """

    try:
        response = model.generate_content(prompt)
        raw_text = response.text

        # Parse sections
        sections = {
            "assessment": "",
            "skills_to_learn": "",
            "resume_tips": "",
            "interview_tips": ""
        }

        if "ASSESSMENT:" in raw_text:
            sections["assessment"] = raw_text.split("ASSESSMENT:")[1].split("SKILLS TO LEARN:")[0].strip()
        if "SKILLS TO LEARN:" in raw_text:
            sections["skills_to_learn"] = raw_text.split("SKILLS TO LEARN:")[1].split("RESUME TIPS:")[0].strip()
        if "RESUME TIPS:" in raw_text:
            sections["resume_tips"] = raw_text.split("RESUME TIPS:")[1].split("INTERVIEW TIPS:")[0].strip()
        if "INTERVIEW TIPS:" in raw_text:
            sections["interview_tips"] = raw_text.split("INTERVIEW TIPS:")[1].strip()

        return {
            "success": True,
            "advice": sections,
            "raw": raw_text
        }

    except Exception as e:
        return {
            "success": False,
            "advice": {},
            "error": str(e)
        }

def get_skill_resources(skill: str) -> dict:
    """Get learning resources for a specific skill"""

    prompt = f"""
    Give me the top 3 FREE online resources to learn {skill} for a job seeker.
    For each resource include:
    - Resource name
    - Website URL
    - Why it's good (one line)
    
    Format as a simple numbered list.
    Be specific and accurate with URLs.
    """

    try:
        response = model.generate_content(prompt)
        return {
            "skill": skill,
            "resources": response.text,
            "success": True
        }
    except Exception as e:
        return {
            "skill": skill,
            "resources": "",
            "success": False,
            "error": str(e)
        }