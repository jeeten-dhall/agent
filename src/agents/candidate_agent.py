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
