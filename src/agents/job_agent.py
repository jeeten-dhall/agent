from agents.base_agent import BaseAgent
from typing import Dict, Any
from langchain.prompts import PromptTemplate


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
        summary = self.run(query)   # natural language summary

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
            json_prompt.format(
                summary=summary,
                job_id=job_id
            )
        )

        return {
            "summary": summary,
            "structured": structured.content
        }
