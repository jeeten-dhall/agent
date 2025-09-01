import json
import re
from typing import Dict, Any
from dotenv import load_dotenv
import os

from agents.base_agent import BaseAgent
from langchain.prompts import PromptTemplate


def _parse_llm_json(raw: str) -> Dict[str, Any]:
    """
    Extract and parse the first valid JSON object/array from the LLM response.
    Cleans away markdown fences and extra explanations.
    """
    try:
        cleaned = raw.strip()

        # Remove fenced code block markers like ```json ... ```
        cleaned = re.sub(r"^```[a-zA-Z]*", "", cleaned, flags=re.MULTILINE)
        cleaned = re.sub(r"```$", "", cleaned, flags=re.MULTILINE).strip()

        # Try to find the first {...} or [...] block
        match = re.search(r"(\{.*\}|\[.*\])", cleaned, flags=re.DOTALL)
        if match:
            return json.loads(match.group(1))

        # If no block is found, attempt direct parsing
        return json.loads(cleaned)

    except Exception as e:
        return {"error": f"Failed to parse JSON: {str(e)}", "raw": raw}


class CandidateAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Candidate")

    def getSkillGap(self, candidate_id: int, job_id: int) -> Dict[str, Any]:
        query = (
            f"What is the skill gap between candidate id {candidate_id} "
            f"and job id {job_id}? Mention the topic and gap pairs in the summary. "
            f"Suggest courses that can fill the gap."
        )
        summary = self.run(query)

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
            json_prompt.format(summary=summary, candidate_id=candidate_id, job_id=job_id)
        )

        return {"summary": summary, "structured": _parse_llm_json(structured.content)}

    def getCareerPath(self, candidate_id: int, desired_job_id: int) -> Dict[str, Any]:
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
            json_prompt.format(summary=summary, candidate_id=candidate_id, desired_job_id=desired_job_id)
        )

        return {"summary": summary, "structured": _parse_llm_json(structured.content)}

    def getSkillsReport(self, candidate_id: int) -> Dict[str, Any]:
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
        structured = self.llm.invoke(json_prompt.format(summary=summary, candidate_id=candidate_id))

        return {"summary": summary, "structured": _parse_llm_json(structured.content)}

    def getRelevantJobsForCandidate(self, candidate_id: int) -> Dict[str, Any]:
        query = (
            f"List the most relevant jobs for candidate id {candidate_id} based on their skills. "
            f"For each job, include a match score, required gaps, and why it is suitable."
        )
        summary = self.run(query)

        json_prompt = PromptTemplate.from_template("""
        Extract structured JSON from the following summary.

        Summary:
        {summary}

        Return JSON with the following format:
        {{
          "candidate_id": {candidate_id},
          "relevant_jobs": [
            {{
              "job_id": int,
              "title": str,
              "match_score": float,
              "missing_topics": [str],
              "explanation": str
            }}
          ]
        }}
        """)
        structured = self.llm.invoke(json_prompt.format(summary=summary, candidate_id=candidate_id))

        return {"summary": summary, "structured": _parse_llm_json(structured.content)}


if __name__ == "__main__":
    agent = CandidateAgent()
    print(agent.getRelevantJobsForCandidate(1))
