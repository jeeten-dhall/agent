from agents.base_agent import BaseAgent
from typing import Dict, Any
from langchain.prompts import PromptTemplate

class CourseAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Course")

    def getCoursesForSkillGap(self, candidate_id: int, job_id: int):
        """
        Ask the agent to recommend courses for filling candidate-job skill gap.
        """
        query = (
            f"Given candidate id {candidate_id} and job id {job_id}, "
            f"which courses best fill the missing topics?"
        )
        return self.run(query)

    def analyzeCourseCoverage(self, course_ids: list, target_topics: list) -> Dict[str, Any]:
        """
        Analyze how well courses cover target skills.
        """
        query = (
            f"Given courses {course_ids} and target topics {target_topics}, "
            f"analyze which skills are covered, which are partially covered, and which are missing."
        )
        summary = self.run(query)

        json_prompt = PromptTemplate.from_template("""
        Extract structured JSON from the following summary.

        Summary:
        {summary}

        Return JSON with the following format:
        {{
          "courses": [ {{ "id": int, "title": str, "covered_topics": [str], "missing_topics": [str] }} ]
        }}
        """)
        structured = self.llm.invoke(
            json_prompt.format(summary=summary)
        )

        return {"summary": summary, "structured": structured.content}

    def suggestNewCourses(self, missing_topics: list) -> Dict[str, Any]:
        """
        Suggest courses to cover missing skills.
        """
        query = (
            f"Suggest new courses that cover the missing topics: {missing_topics}. "
            f"Provide course title, topics, and expected skill level."
        )
        summary = self.run(query)

        json_prompt = PromptTemplate.from_template("""
        Extract structured JSON from the following summary.
    
        Summary:
        {summary}
    
        Return JSON with the following format:
        {{
          "suggested_courses": [ {{ "title": str, "topics": [str], "skill_level": str }} ]
        }}
        """)
        structured = self.llm.invoke(
            json_prompt.format(summary=summary)
        )

        return {"summary": summary, "structured": structured.content}

if __name__ == "__main__":
    course_agent = CourseAgent()

    # print(course_agent.getCoursesForSkillGap(1, 101))
    # print(course_agent.analyzeCourseCoverage([201, 202], ["Data Structures", "Linear Algebra"]))
    print(course_agent.suggestNewCourses(["Linear Algebra", "Probability", "Deep Learning", "Large-Language Models"]))
