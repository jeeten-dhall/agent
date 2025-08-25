import json
import os
import re

# Resolve path relative to this script’s folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CANDIDATES_FILE = os.path.join(BASE_DIR, "../../data/candidates.json")

def get_candidate_topics(input_str: str):
    """
    Tool function for LangChain.
    Input: candidate_id as string or number (e.g. "1" or "candidate_id=1").
    Returns: dict with candidate info + topics.
    """
    match = re.search(r"\d+", str(input_str))
    if not match:
        return {"error": "No candidate_id provided"}

    candidate_id = int(match.group())

    if not os.path.exists(CANDIDATES_FILE):
        return {"error": f"File {CANDIDATES_FILE} not found"}

    with open(CANDIDATES_FILE, "r") as f:
        candidates = json.load(f)

    for cand in candidates:
        if cand["id"] == candidate_id:
            return cand

    return {"error": f"Candidate with id={candidate_id} not found"}


# -----------------------
# Test block
# -----------------------
if __name__ == "__main__":
    print("Testing get_candidate_topics...\n")

    # Test with existing candidate
    result1 = get_candidate_topics("1")
    print("Input: '1'")
    print("Output:", result1, "\n")

    # Test with 'candidate_id=2'
    result2 = get_candidate_topics("candidate_id=2")
    print("Input: 'candidate_id=2'")
    print("Output:", result2, "\n")

    # Test with non-existent candidate
    result3 = get_candidate_topics("99")
    print("Input: '99'")
    print("Output:", result3, "\n")

    # Test with invalid input
    result4 = get_candidate_topics("abc")
    print("Input: 'abc'")
    print("Output:", result4, "\n")
