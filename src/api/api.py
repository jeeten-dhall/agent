from fastapi import FastAPI
from dotenv import load_dotenv
import os

# ✅ make sure env is loaded when uvicorn starts
load_dotenv()

from agents.candidate_agent import CandidateAgent
from agents.job_agent import JobAgent

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Agent API is running"}

@app.get("/candidate/{candidate_id}/job/{job_id}/skill-gap")
def skill_gap(candidate_id: int, job_id: int):
    agent = CandidateAgent()
    result = agent.getSkillGap(candidate_id, job_id)
    return {
        "summary": result.get("summary") if isinstance(result, dict) else str(result),
        "structured": result
    }


@app.get("/job/{job_id}/matching-candidates")
def matching_candidates(job_id: int):
    agent = JobAgent()
    result = agent.getMatchingCandidates(job_id)
    return {
        "summary": result.get("summary") if isinstance(result, dict) else str(result),
        "structured": result
    }