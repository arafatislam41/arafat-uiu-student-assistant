import json
from pathlib import Path

PROFILE_FILE = Path(__file__).resolve().parent.parent / "data" / "profile.json"

def load_profile():
    """Load the user profile from JSON."""
    if not PROFILE_FILE.exists():
        return {
            "name": "Guest",
            "student_id": "N/A",
            "current_cgpa": 0.0,
            "completed_credits": 0.0,
            "history": []
        }
    with open(PROFILE_FILE, "r", encoding="utf-8-sig") as file:
        return json.load(file)

def save_profile(data):
    """Save the user profile to JSON."""
    PROFILE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PROFILE_FILE, "w", encoding="utf-8-sig") as file:
        json.dump(data, file, indent=4)

def get_profile():
    return load_profile()

def update_profile(name=None, student_id=None, cgpa=None, credits=None):
    profile = load_profile()
    if name is not None: profile["name"] = name
    if student_id is not None: profile["student_id"] = student_id
    if cgpa is not None: profile["current_cgpa"] = float(cgpa)
    if credits is not None: profile["completed_credits"] = float(credits)
    save_profile(profile)

