from fastapi import FastAPI, Query
from dotenv import load_dotenv
from typing import List
import json
import os

from api.cache import cache_key, cache_get, cache_set

# ✅ load .env
load_dotenv()

from agents.candidate_agent import CandidateAgent
from agents.job_agent import JobAgent
from agents.course_agent import CourseAgent

# -------------------
# Data files
# -------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

CANDIDATES_FILE = os.path.join(DATA_DIR, "candidates.json")
JOBS_FILE = os.path.join(DATA_DIR, "jobs.json")
COURSES_FILE = os.path.join(DATA_DIR, "courses.json")

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Agent API is running"}

# ======================================================
# CandidateAgent endpoints
# ======================================================

@app.get("/candidate/{candidate_id}/job/{job_id}/skill-gap")
def skill_gap(candidate_id: int, job_id: int):
    key = cache_key("skill_gap", {"candidate_id": candidate_id, "job_id": job_id})
    cached = cache_get(key)
    if cached:
        return cached
    agent = CandidateAgent()
    result = agent.getSkillGap(candidate_id, job_id)
    cache_set(key, result)
    return result

@app.get("/candidate/{candidate_id}/career-path/{desired_job_id}")
def candidate_career_path(candidate_id: int, desired_job_id: int):
    key = cache_key("career_path", {"candidate_id": candidate_id, "desired_job_id": desired_job_id})
    cached = cache_get(key)
    if cached:
        return cached
    agent = CandidateAgent()
    result = agent.getCareerPath(candidate_id, desired_job_id)
    cache_set(key, result)
    return result

@app.get("/candidate/{candidate_id}/skills-report")
def candidate_skills_report(candidate_id: int):
    key = cache_key("skills_report", {"candidate_id": candidate_id})
    cached = cache_get(key)
    if cached:
        return cached
    agent = CandidateAgent()
    result = agent.getSkillsReport(candidate_id)
    cache_set(key, result)
    return result

# ======================================================
# JobAgent endpoints
# ======================================================

@app.get("/job/{job_id}/matching-candidates")
def job_matching_candidates(job_id: int):
    key = cache_key("matching_candidates", {"job_id": job_id})
    cached = cache_get(key)
    if cached:
        return cached
    agent = JobAgent()
    result = agent.getMatchingCandidates(job_id)
    cache_set(key, result)
    return result

@app.get("/job/{job_id}/candidate/{candidate_id}/skills-report")
def job_candidate_skills_report(candidate_id: int, job_id: int):
    key = cache_key("job_candidate_skills_report", {"candidate_id": candidate_id, "job_id": job_id})
    cached = cache_get(key)
    if cached:
        return cached
    agent = JobAgent()
    result = agent.getSkillsReportAndJobReadiness(candidate_id, job_id)
    cache_set(key, result)
    return result

@app.get("/job/{job_id}/explain-ranking")
def job_explain_ranking(job_id: int):
    key = cache_key("explain_ranking", {"job_id": job_id})
    cached = cache_get(key)
    if cached:
        return cached
    agent = JobAgent()
    result = agent.explainCandidateRanking(job_id)
    cache_set(key, result)
    return result

# ======================================================
# CourseAgent endpoints
# ======================================================

@app.get("/courses/recommendations/candidate/{candidate_id}/job/{job_id}")
def course_recommendations(candidate_id: int, job_id: int):
    key = cache_key("course_recommendations", {"candidate_id": candidate_id, "job_id": job_id})
    cached = cache_get(key)
    if cached:
        return cached
    agent = CourseAgent()
    result = agent.getCoursesForSkillGap(candidate_id, job_id)
    cache_set(key, result)
    return result

@app.get("/courses/analyze-coverage")
def analyze_course_coverage(
    course_ids: List[int] = Query(..., description="List of course IDs"),
    target_topics: List[str] = Query(..., description="List of target topics"),
):
    key = cache_key("analyze_coverage", {"course_ids": course_ids, "target_topics": target_topics})
    cached = cache_get(key)
    if cached:
        return cached
    agent = CourseAgent()
    result = agent.analyzeCourseCoverage(course_ids, target_topics)
    cache_set(key, result)
    return result

@app.get("/courses/suggest-new")
def suggest_new_courses(
    missing_topics: List[str] = Query(..., description="List of missing topics"),
):
    key = cache_key("suggest_new_courses", {"missing_topics": missing_topics})
    cached = cache_get(key)
    if cached:
        return cached
    agent = CourseAgent()
    result = agent.suggestNewCourses(missing_topics)
    cache_set(key, result)
    return result

# ======================================================
# NEW: direct JSON data endpoints (no cache)
# ======================================================

@app.get("/candidates")
def get_all_candidates():
    if not os.path.exists(CANDIDATES_FILE):
        return {"error": f"{CANDIDATES_FILE} not found"}
    with open(CANDIDATES_FILE, "r") as f:
        return json.load(f)

@app.get("/jobs")
def get_all_jobs():
    if not os.path.exists(JOBS_FILE):
        return {"error": f"{JOBS_FILE} not found"}
    with open(JOBS_FILE, "r") as f:
        return json.load(f)

@app.get("/courses")
def get_all_courses():
    if not os.path.exists(COURSES_FILE):
        return {"error": f"{COURSES_FILE} not found"}
    with open(COURSES_FILE, "r") as f:
        return json.load(f)
