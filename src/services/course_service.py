import json
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COURSES_FILE = os.path.join(BASE_DIR, "../../data/courses.json")

def get_course_details(input_str: str):
    """
    Get course details by course_id.
    Input: string or number (e.g. "201" or "course_id=201")
    Returns: dict with course info.
    """
    match = re.search(r"\d+", str(input_str))
    if not match:
        return {"error": "No course_id provided"}

    course_id = int(match.group())

    if not os.path.exists(COURSES_FILE):
        return {"error": f"File {COURSES_FILE} not found"}

    with open(COURSES_FILE, "r") as f:
        courses = json.load(f)

    for course in courses:
        if course["id"] == course_id:
            return course

    return {"error": f"Course with id={course_id} not found"}


def search_courses_by_topic(topic: str):
    """
    Search for courses that cover a given topic.
    Input: topic name (e.g. "Probability").
    Returns: list of matching courses.
    """
    if not os.path.exists(COURSES_FILE):
        return {"error": f"File {COURSES_FILE} not found"}

    with open(COURSES_FILE, "r") as f:
        courses = json.load(f)

    matches = [c for c in courses if topic in c["topics"]]

    if not matches:
        return {"error": f"No courses found for topic '{topic}'"}

    return matches
