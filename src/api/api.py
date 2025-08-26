from fastapi import FastAPI, Query
from dotenv import load_dotenv
from typing import List

# ✅ make sure env is loaded when uvicorn starts
load_dotenv()

from agents.candidate_agent import CandidateAgent
from agents.job_agent import JobAgent
from agents.course_agent import CourseAgent

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Agent API is running"}

# ---------------- CandidateAgent ----------------

@app.get("/candidate/{candidate_id}/job/{job_id}/skill-gap")
def candidate_skill_gap(candidate_id: int, job_id: int):
    agent = CandidateAgent()
    result = agent.getSkillGap(candidate_id, job_id)
    return result

@app.get("/candidate/{candidate_id}/career-path/{desired_job_id}")
def candidate_career_path(candidate_id: int, desired_job_id: int):
    agent = CandidateAgent()
    result = agent.getCareerPath(candidate_id, desired_job_id)
    return result

@app.get("/candidate/{candidate_id}/skills-report")
def candidate_skills_report(candidate_id: int):
    agent = CandidateAgent()
    result = agent.getSkillsReport(candidate_id)
    return result

# ---------------- JobAgent ----------------

@app.get("/job/{job_id}/matching-candidates")
def job_matching_candidates(job_id: int):
    agent = JobAgent()
    result = agent.getMatchingCandidates(job_id)
    return result

@app.get("/job/{job_id}/candidate/{candidate_id}/skills-report")
def job_candidate_skills_report(candidate_id: int, job_id: int):
    agent = JobAgent()
    result = agent.getSkillsReportAndJobReadiness(candidate_id, job_id)
    return result

@app.get("/job/{job_id}/explain-ranking")
def job_explain_ranking(job_id: int):
    agent = JobAgent()
    result = agent.explainCandidateRanking(job_id)
    return result

# ---------------- CourseAgent ----------------

@app.get("/courses/recommendations/candidate/{candidate_id}/job/{job_id}")
def course_recommendations(candidate_id: int, job_id: int):
    agent = CourseAgent()
    result = agent.getCoursesForSkillGap(candidate_id, job_id)
    return result

@app.get("/courses/analyze-coverage")
def analyze_course_coverage(
    course_ids: List[int] = Query(..., description="List of course IDs"),
    target_topics: List[str] = Query(..., description="List of target topics"),
):
    agent = CourseAgent()
    result = agent.analyzeCourseCoverage(course_ids, target_topics)
    return result

@app.get("/courses/suggest-new")
def suggest_new_courses(
    missing_topics: List[str] = Query(..., description="List of missing topics"),
):
    agent = CourseAgent()
    result = agent.suggestNewCourses(missing_topics)
    return result
