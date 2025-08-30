import json
import os
import re

# Resolve path relative to this script’s folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JOBS_FILE = os.path.join(BASE_DIR, "../../data/jobs.json")

def get_job_requirements(input_str: str):
    """
    Tool function for LangChain.
    Input: job_id as string or number (e.g. "101" or "job_id=101").
    Returns: dict with job info (id, title, required_topics).
    """
    match = re.search(r"\d+", str(input_str))
    if not match:
        return {"error": "No job_id provided"}

    job_id = int(match.group())

    if not os.path.exists(JOBS_FILE):
        return {"error": f"File {JOBS_FILE} not found"}

    with open(JOBS_FILE, "r") as f:
        jobs = json.load(f)

    for job in jobs:
        if job["id"] == job_id:
            return job

    return {"error": f"Job with id={job_id} not found"}

def list_jobs(input_str: str = None):
    """
    Return list of all jobs.
    LangChain Tool passes an argument, so input_str is optional and ignored.
    """
    if not os.path.exists(JOBS_FILE):
        return {"error": f"File {JOBS_FILE} not found"}

    with open(JOBS_FILE, "r") as f:
        return json.load(f)

def get_job_by_id(job_id: int):
    """
    Return job dict for a given job_id.
    """
    if not os.path.exists(JOBS_FILE):
        return {"error": f"File {JOBS_FILE} not found"}

    with open(JOBS_FILE, "r") as f:
        jobs = json.load(f)

    for job in jobs:
        if job["id"] == job_id:
            return job

    return {"error": f"Job with id={job_id} not found"}

# -----------------------
# Test block
# -----------------------
if __name__ == "__main__":
    print("Testing get_job_requirements...\n")

    # Test with existing job
    result1 = get_job_requirements("101")
    print("Input: '101'")
    print("Output:", result1, "\n")

    # Test with 'job_id=102'
    result2 = get_job_requirements("job_id=102")
    print("Input: 'job_id=102'")
    print("Output:", result2, "\n")

    # Test with non-existent job
    result3 = get_job_requirements("999")
    print("Input: '999'")
    print("Output:", result3, "\n")

    # Test with invalid input
    result4 = get_job_requirements("abc")
    print("Input: 'abc'")
    print("Output:", result4, "\n")

    result5 = list_jobs()
    print("List of jobs:")
    print(result5)

    # --- Test get_job_by_id ---
    print("6. get_job_by_id(101):")
    print(get_job_by_id(101), "\n")

    print("7. get_job_by_id(999) (non-existent):")
    print(get_job_by_id(999), "\n")