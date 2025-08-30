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
    topic = topic.strip().strip("'\"")  # remove stray quotes

    if not os.path.exists(COURSES_FILE):
        return {"error": f"File {COURSES_FILE} not found"}

    with open(COURSES_FILE, "r") as f:
        courses = json.load(f)

    matches = [c for c in courses if topic in c["topics"]]

    if not matches:
        return {"error": f"No courses found for topic '{topic}'"}

    return matches

def list_courses(input_str: str = None):
    """
    Return list of all courses.
    LangChain Tool passes an argument, so input_str is optional and ignored.
    """
    if not os.path.exists(COURSES_FILE):
        return {"error": f"File {COURSES_FILE} not found"}

    with open(COURSES_FILE, "r") as f:
        return json.load(f)

# -----------------------
# Test block
# -----------------------
if __name__ == "__main__":
    print("Testing Course Service functions...\n")

    # --- Test get_course_details ---
    print("1. get_course_details('201'):")
    print(get_course_details("201"), "\n")

    print("2. get_course_details('course_id=202'):")
    print(get_course_details("course_id=202"), "\n")

    print("3. get_course_details('999') (non-existent course):")
    print(get_course_details("999"), "\n")

    print("4. get_course_details('abc') (invalid input):")
    print(get_course_details("abc"), "\n")

    # --- Test search_courses_by_topic ---
    print("5. search_courses_by_topic('Probability'):")
    print(search_courses_by_topic("Probability"), "\n")

    print("6. search_courses_by_topic('Machine Learning'):")
    print(search_courses_by_topic("Machine Learning"), "\n")

    print("7. search_courses_by_topic('NonExistentTopic'):")
    print(search_courses_by_topic("NonExistentTopic"), "\n")

    # --- Test list_courses ---
    print("8. list_courses():")
    print(list_courses(), "\n")
