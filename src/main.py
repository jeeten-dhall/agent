from dotenv import load_dotenv
import os

from agents.candidate_agent import CandidateAgent
from agents.job_agent import JobAgent
from agents.course_agent import CourseAgent

if __name__ == "__main__":
    load_dotenv()  # take variables from .env
    api_key = os.getenv("OPENAI_API_KEY")
    print("API Key loaded:", api_key[:15] + "*****")

    candidate_agent = CandidateAgent()
    # job_agent = JobAgent()
    # course_agent = CourseAgent()

    # Candidate perspective
    print(candidate_agent.getSkillGap(1, 101))

    # Recruiter perspective
    # print(job_agent.getMatchingCandidates(101))

    # Content provider perspective
    # print(course_agent.getCoursesForSkillGap(1, 101))
