import json
import re
from typing import Dict, Any
from langchain.prompts import PromptTemplate
from agents.base_agent import BaseAgent

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


class JobAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Job")

    def getMatchingCandidates(self, job_id: int) -> Dict[str, Any]:
        """
        Find candidates matching a job and return both structured data and summary.
        """
        query = (
            f"Which candidate ids closely match job id {job_id}? "
            f"Provide candidate IDs with their match score. "
            f"Also mention why they are a good fit in the explanation."
        )
        summary = self.run(query)  # natural language summary

        # Ask LLM to return JSON structure from that summary
        json_prompt = PromptTemplate.from_template("""
        Extract structured JSON from the following summary.

        Summary:
        {summary}

        Return JSON with the following format:
        {{
          "job_id": {job_id},
          "matches": [ {{ "candidate_id": int, "score": float }} ],
          "explanation": str
        }}
        """)
        structured = self.llm.invoke(
            json_prompt.format(summary=summary, job_id=job_id)
        )

        return {
            "summary": summary,
            "structured": _parse_llm_json(structured.content)
        }

    def getSkillsReportAndJobReadiness(self, candidate_id: int, job_id: int) -> Dict[str, Any]:
        """
        Generate candidate's skill report.
        """
        query = (
            f"Candidate id {candidate_id}: summarize strengths, weaknesses, and opportunities in topics "
            f"with respect to job id {job_id}. Also mention the timeline by which the candidate will be ready, "
            f"suggest some courses the candidate should take during that time."
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
          "strengths": [ {{ "topic": str, "score": float }} ],
          "weaknesses": [ {{ "topic": str, "score": float }} ],
          "opportunities": [ {{ "topic": str, "recommendation": str }} ]
        }}
        """)
        structured = self.llm.invoke(
            json_prompt.format(summary=summary, candidate_id=candidate_id, job_id=job_id)
        )

        return {"summary": summary, "structured": _parse_llm_json(structured.content)}

    def explainCandidateRanking(self, job_id: int) -> Dict[str, Any]:
        """
        For candidates matched to a job, provide reasoning for their scores.
        """
        query = f"For job id {job_id}, explain why each candidate is a strong or weak match."
        summary = self.run(query)

        json_prompt = PromptTemplate.from_template("""
        Extract structured JSON from the following summary.

        Summary:
        {summary}

        Return JSON with the following format:
        {{
          "job_id": {job_id},
          "candidate_rankings": [ {{ "candidate_id": int, "score": float, "reason": str }} ]
        }}
        """)
        structured = self.llm.invoke(
            json_prompt.format(summary=summary, job_id=job_id)
        )

        return {"summary": summary, "structured": _parse_llm_json(structured.content)}


if __name__ == "__main__":
    job_agent = JobAgent()

    # print(job_agent.getMatchingCandidates(101))
    # print(job_agent.getSkillsReportAndJobReadiness(1, 101))
    print(job_agent.explainCandidateRanking(101))
