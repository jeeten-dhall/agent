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

    def getCourseImprovementSuggestions(self, course_id: int) -> Dict[str, Any]:
        """
        Suggest improvements for a given course by comparing it with job requirements
        and candidate skill gaps.
        """
        query = (
            f"Analyze course with id {course_id}. "
            f"Compare its covered topics with job requirements and candidate skill gaps. "
            f"Suggest improvements to the course such as adding missing topics, updating outdated topics, "
            f"or providing more practical exercises."
        )
        summary = self.run(query)

        json_prompt = PromptTemplate.from_template("""
        Extract structured JSON from the following summary.
    
        Summary:
        {summary}
    
        Return JSON with the following format:
        {{
          "course_id": int,
          "improvements": [str],
          "missing_topics": [str],
          "outdated_topics": [str],
          "practical_exercises": [str]
        }}
        """)
        structured = self.llm.invoke(json_prompt.format(summary=summary))

        return {"summary": summary, "structured": structured.content}

    def getMostInDemandTopics(self) -> Dict[str, Any]:
        """
        Identify the most in-demand topics across all jobs,
        regardless of whether courses already cover them.
        """
        query = (
            "Analyze the job requirements across all jobs. "
            "Identify the most frequently requested topics and skills in the job market. "
            "Rank them by demand, without considering existing course coverage."
        )
        summary = self.run(query)

        json_prompt = PromptTemplate.from_template("""
        Extract structured JSON from the following summary.

        Summary:
        {summary}

        Return JSON with the following format:
        {{
          "in_demand_topics": [{{ "topic": str, "demand_score": int }}]
        }}
        """)
        structured = self.llm.invoke(json_prompt.format(summary=summary))

        return {"summary": summary, "structured": structured.content}

    def getCourseMarketFit(self, course_id: int) -> Dict[str, Any]:
        """
        Evaluate how well a given course matches industry demand and candidate needs.
        """
        query = (
            f"Evaluate course with id {course_id} against the skill requirements in jobs and current candidate skills. "
            f"Determine how well this course addresses market demand and where it falls short."
        )
        summary = self.run(query)

        json_prompt = PromptTemplate.from_template("""
        Extract structured JSON from the following summary.
    
        Summary:
        {summary}
    
        Return JSON with the following format:
        {{
          "course_id": int,
          "strengths": [str],
          "gaps": [str],
          "market_fit_score": int
        }}
        """)
        structured = self.llm.invoke(json_prompt.format(summary=summary))

        return {"summary": summary, "structured": structured.content}


    def getCourseCompetitorAnalysis(self, course_id: int) -> Dict[str, Any]:
        """
        Compare a course with other courses covering similar topics.
        Highlight strengths, weaknesses, and unique differentiators.
        """
        query = (
            f"Compare course with id {course_id} against other courses covering similar topics. "
            f"Highlight strengths, weaknesses, and unique differentiators of this course."
        )
        summary = self.run(query)

        json_prompt = PromptTemplate.from_template("""
        Extract structured JSON from the following summary.
    
        Summary:
        {summary}
    
        Return JSON with the following format:
        {{
          "course_id": int,
          "competitors": [{{ "id": int, "title": str }}],
          "strengths": [str],
          "weaknesses": [str],
          "unique_differentiators": [str]
        }}
        """)
        structured = self.llm.invoke(json_prompt.format(summary=summary))

        return {"summary": summary, "structured": structured.content}


    def getEmergingTopicsForCourses(self) -> Dict[str, Any]:
        """
        Identify emerging or trending topics in jobs that are not yet adequately covered by existing courses.
        """
        query = (
            "Identify emerging or trending topics in jobs that are not yet adequately covered by existing courses. "
            "Recommend new areas where course creators should develop content."
        )
        summary = self.run(query)

        json_prompt = PromptTemplate.from_template("""
        Extract structured JSON from the following summary.
    
        Summary:
        {summary}
    
        Return JSON with the following format:
        {{
          "emerging_topics": [str],
          "recommended_course_ideas": [{{ "title": str, "topics": [str], "target_audience": str }}]
        }}
        """)
        structured = self.llm.invoke(json_prompt.format(summary=summary))

        return {"summary": summary, "structured": structured.content}


if __name__ == "__main__":
    course_agent = CourseAgent()

    # print(course_agent.getCoursesForSkillGap(1, 101))
    # print(course_agent.analyzeCourseCoverage([201, 202], ["Data Structures", "Linear Algebra"]))
    # print(course_agent.suggestNewCourses(["Linear Algebra", "Probability", "Deep Learning", "Large-Language Models"]))

    # Test: recommend improvements for a given course
    print("\n--- getCourseImprovementSuggestions ---")
    print(course_agent.getCourseImprovementSuggestions(201))

    # Test: identify most in-demand topics not covered by courses
    print("\n--- getMostInDemandTopics ---")
    print(course_agent.getMostInDemandTopics())

    # Test: evaluate course market fit
    print("\n--- getCourseMarketFit ---")
    print(course_agent.getCourseMarketFit(202))

    # Test: competitor analysis for a course
    print("\n--- getCourseCompetitorAnalysis ---")
    print(course_agent.getCourseCompetitorAnalysis(203))

    # Test: emerging topics for new course creation
    print("\n--- getEmergingTopicsForCourses ---")
    print(course_agent.getEmergingTopicsForCourses())