import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_openai import ChatOpenAI
from services.candidate_service import get_candidate_topics
from services.job_service import get_job_requirements
from services.course_service import get_course_details, search_courses_by_topic


class BaseAgent:
    def __init__(self, name, llm=None, verbose=True, model="gpt-4o-mini"):
        self.name = name

        load_dotenv()  # take variables from .env
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set. Did you load .env?")

        # ✅ All services available to every agent
        self.tools = [
            Tool(
                name="Candidate Service",
                func=get_candidate_topics,
                description="Get candidate info by candidate_id. Returns JSON with id, name, and topics with scores."
            ),
            Tool(
                name="Job Service",
                func=get_job_requirements,
                description="Get job requirements by job_id. Returns JSON with id, title, and required_topics with scores."
            ),
            Tool(
                name="Course Service",
                func=get_course_details,
                description="Get course details by course_id. Returns JSON with id, title, and topics list."
            ),
            Tool(
                name="Course Search",
                func=search_courses_by_topic,
                description="Search for courses covering a given topic. Input is topic name (e.g. 'Probability')."
            )
        ]

        # ✅ Default LLM is ChatOpenAI with GPT-4o-mini
        self.llm = llm or ChatOpenAI(
            model=model,
            temperature=0,
            api_key=api_key
        )

        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=verbose
        )

    def run(self, query: str):
        print(f"\n[{self.name} Agent] Running query: {query}")
        return self.agent.run(query)
