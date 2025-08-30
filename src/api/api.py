from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import List
import json
import os

from api.cache import cache_key, cache_get, cache_set

# ✅ load .env
load_dotenv()

from services.candidate_service import list_candidates, get_candidate_by_id
from services.job_service import list_jobs, get_job_by_id
from services.course_service import list_courses, get_course_by_id

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

# ✅ Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your frontend URL
    allow_credentials=True,
    allow_methods=["*"],   # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],   # allow all headers
)

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

@app.get("/candidate/{candidate_id}/relevant-jobs")
def candidate_relevant_jobs(candidate_id: int):
    key = cache_key("relevant_jobs", {"candidate_id": candidate_id})
    cached = cache_get(key)
    if cached:
        return cached
    agent = CandidateAgent()
    result = agent.getRelevantJobsForCandidate(candidate_id)
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
# New CourseAgent endpoints
# ======================================================

@app.get("/course/{course_id}/improvement-suggestions")
def course_improvement_suggestions(course_id: int):
    key = cache_key("course_improvement_suggestions", {"course_id": course_id})
    cached = cache_get(key)
    if cached:
        return cached
    agent = CourseAgent()
    result = agent.getCourseImprovementSuggestions(course_id)
    cache_set(key, result)
    return result


@app.get("/courses/most-in-demand-topics")
def courses_most_in_demand_topics():
    key = cache_key("courses_most_in_demand_topics", {})
    cached = cache_get(key)
    if cached:
        return cached
    agent = CourseAgent()
    result = agent.getMostInDemandTopics()
    cache_set(key, result)
    return result


@app.get("/course/{course_id}/market-fit")
def course_market_fit(course_id: int):
    key = cache_key("course_market_fit", {"course_id": course_id})
    cached = cache_get(key)
    if cached:
        return cached
    agent = CourseAgent()
    result = agent.getCourseMarketFit(course_id)
    cache_set(key, result)
    return result


@app.get("/course/{course_id}/competitor-analysis")
def course_competitor_analysis(course_id: int):
    key = cache_key("course_competitor_analysis", {"course_id": course_id})
    cached = cache_get(key)
    if cached:
        return cached
    agent = CourseAgent()
    result = agent.getCourseCompetitorAnalysis(course_id)
    cache_set(key, result)
    return result


@app.get("/courses/emerging-topics")
def courses_emerging_topics():
    key = cache_key("courses_emerging_topics", {})
    cached = cache_get(key)
    if cached:
        return cached
    agent = CourseAgent()
    result = agent.getEmergingTopicsForCourses()
    cache_set(key, result)
    return result

# ======================================================
# NEW: direct JSON data endpoints (no cache)
# ======================================================

@app.get("/candidates")
def get_all_candidates():
    return list_candidates()

@app.get("/jobs")
def get_all_jobs():
    return list_jobs()

@app.get("/courses")
def get_all_courses():
    return list_courses()

@app.get("/candidates/{candidate_id}")
def get_candidate(candidate_id: int):
    key = cache_key("get_candidate", {"candidate_id": candidate_id})
    cached = cache_get(key)
    if cached:
        return cached
    result = get_candidate_by_id(candidate_id)
    cache_set(key, result)
    return result

@app.get("/courses/{course_id}")
def get_course(course_id: int):
    key = cache_key("get_course", {"course_id": course_id})
    cached = cache_get(key)
    if cached:
        return cached
    result = get_course_by_id(course_id)
    cache_set(key, result)
    return result

@app.get("/jobs/{job_id}")
def get_job(job_id: int):
    key = cache_key("get_job", {"job_id": job_id})
    cached = cache_get(key)
    if cached:
        return cached
    result = get_job_by_id(job_id)
    cache_set(key, result)
    return result