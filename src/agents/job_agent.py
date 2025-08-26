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

    def getSkillsReportAndJobReadiness(self, candidate_id: int, job_id: int) -> Dict[str, Any]:
        """
        Generate candidate's skill report.
        """
        query = f"Candidate id {candidate_id}: summarize strengths, weaknesses, and opportunities in topics with respect to job id {job_id}. Also mention the timeline by which the candidate will be ready, suggest some courses the candidate should take during that time."
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
            json_prompt.format(summary=summary, candidate_id=candidate_id, job_id = job_id)
        )

        return {"summary": summary, "structured": structured.content}

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

        return {"summary": summary, "structured": structured.content}

if __name__ == "__main__":
    job_agent = JobAgent()

    # print(job_agent.getMatchingCandidates(101))

    # print(job_agent.getSkillsReportAndJobReadiness(1, 101))

    print(job_agent.explainCandidateRanking(101))
