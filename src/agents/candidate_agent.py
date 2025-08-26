from dotenv import load_dotenv
import os

from agents.base_agent import BaseAgent

from typing import Dict, Any
from langchain.prompts import PromptTemplate

class CandidateAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Candidate")

    def getSkillGap(self, candidate_id: int, job_id: int) -> Dict[str, Any]:
        """
        Compute skill gap between a candidate and a job.
        Returns dict with both structured data and summary.
        """
        query = (
            f"What is the skill gap between candidate id {candidate_id} "
            f"and job id {job_id}? Mention the topic and gap pairs in the summary. Suggest courses that can fill the gap."
        )
        print("Running first query to agent...")
        summary = self.run(query)   # natural language summary
        print("Got summary:", summary)

        # Ask LLM to return JSON structure from that summary
        json_prompt = PromptTemplate.from_template("""
        Extract structured JSON from the following summary.

        Summary:
        {summary}

        Return JSON with the following format:
        {{
          "candidate_id": {candidate_id},
          "job_id": {job_id},
          "gaps": [ {{ "topic": str, "gap": float }} ],
          "courses": [ {{ "id": int, "title": str, "topics": [str] }} ],
          "explanation": str
        }}
        """)
        structured = self.llm.invoke(
            json_prompt.format(
                summary=summary,
                candidate_id=candidate_id,
                job_id=job_id
            )
        )

        return {
            "summary": summary,
            "structured": structured.content
        }

    def getCareerPath(self, candidate_id: int, desired_job_id: int) -> Dict[str, Any]:
        """
        Suggest a step-by-step career path or learning plan to reach the desired job.
        Returns summary and structured JSON.
        """
        query = (
            f"Candidate id {candidate_id} wants to become job id {desired_job_id}. "
            f"Suggest a learning path and milestones with timelines."
        )
        summary = self.run(query)

        json_prompt = PromptTemplate.from_template("""
        Extract structured JSON from the following summary.

        Summary:
        {summary}

        Return JSON with the following format:
        {{
          "candidate_id": {candidate_id},
          "job_id": {desired_job_id},
          "milestones": [ {{ "topic": str, "target_level": float, "suggested_courses": [str] }} ],
          "timeline_months": int,
          "explanation": str
        }}
        """)
        structured = self.llm.invoke(
            json_prompt.format(
                summary=summary,
                candidate_id=candidate_id,
                desired_job_id=desired_job_id
            )
        )

        return {"summary": summary, "structured": structured.content}

    def getSkillsReport(self, candidate_id: int) -> Dict[str, Any]:
        """
        Generate candidate's skill report.
        """
        query = f"Candidate id {candidate_id}: summarize strengths, weaknesses, and opportunities in topics."
        summary = self.run(query)

        json_prompt = PromptTemplate.from_template("""
        Extract structured JSON from the following summary.

        Summary:
        {summary}

        Return JSON with the following format:
        {{
          "candidate_id": {candidate_id},
          "strengths": [ {{ "topic": str, "score": float }} ],
          "weaknesses": [ {{ "topic": str, "score": float }} ],
          "opportunities": [ {{ "topic": str, "recommendation": str }} ]
        }}
        """)
        structured = self.llm.invoke(
            json_prompt.format(summary=summary, candidate_id=candidate_id)
        )

        return {"summary": summary, "structured": structured.content}

if __name__ == "__main__":
    candidate_agent = CandidateAgent()

    # print(candidate_agent.getSkillGap(1, 101))

    # print(candidate_agent.getCareerPath(1, 101))
    print(candidate_agent.getSkillsReport(1))

