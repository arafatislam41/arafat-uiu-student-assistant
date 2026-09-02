import json
from config import get_user_data_dir

PROFILE_FILE = get_user_data_dir() / "profile.json"

DEFAULT_GUEST_PROFILE = {
    "name": "Guest Student",
    "student_id": "Not Set",
    "department": "CSE",
    "current_cgpa": 0.00,
    "completed_credits": 0.0,
    "is_first_run": True
}

def get_profile() -> dict:
    if not PROFILE_FILE.exists():
        return DEFAULT_GUEST_PROFILE.copy()
    try:
        with open(PROFILE_FILE, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
            # Ensure all keys exist
            merged = DEFAULT_GUEST_PROFILE.copy()
            merged.update(data)
            return merged
    except Exception:
        return DEFAULT_GUEST_PROFILE.copy()

def update_profile(name=None, student_id=None, department=None, cgpa=None, credits=None, is_first_run=None):
    prof = get_profile()
    if name is not None: prof["name"] = name.strip()
    if student_id is not None: prof["student_id"] = student_id.strip()
    if department is not None: prof["department"] = department.strip().upper()
    if cgpa is not None: prof["current_cgpa"] = float(cgpa)
    if credits is not None: prof["completed_credits"] = float(credits)
    if is_first_run is not None: prof["is_first_run"] = bool(is_first_run)

    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(prof, f, indent=2)
    return prof

def reset_to_guest():
    """Resets user configuration back to guest defaults."""
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_GUEST_PROFILE, f, indent=2)
    return DEFAULT_GUEST_PROFILE.copy()
