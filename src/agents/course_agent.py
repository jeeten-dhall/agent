from agents.base_agent import BaseAgent

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
