import json
from config import get_data_dir

COURSES_FILE = get_data_dir() / "courses.json"

def _load_courses():
    if not COURSES_FILE.exists():
        return {}
    with open(COURSES_FILE, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def normalize_code(code: str) -> str:
    cleaned = code.strip().upper().replace(" ", "")
    for i, c in enumerate(cleaned):
        if c.isdigit():
            return f"{cleaned[:i]} {cleaned[i:]}"
    return cleaned

def get_course_info(code: str):
    courses = _load_courses()
    norm = normalize_code(code)
    for c_code, details in courses.items():
        if normalize_code(c_code) == norm:
            return details
    return None

def list_courses():
    return _load_courses()

def check_prerequisites(target_code: str, completed_codes: list[str]) -> dict:
    info = get_course_info(target_code)
    if not info:
        return {"can_take": True, "missing": []}
    
    prereqs = [normalize_code(p) for p in info.get("prerequisites", [])]
    completed_norm = [normalize_code(c) for c in completed_codes]
    
    missing = [p for p in prereqs if p not in completed_norm]
    return {
        "can_take": len(missing) == 0,
        "missing": missing
    }
