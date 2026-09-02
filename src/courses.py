import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "courses.json"


def _load_courses():
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, "r", encoding="utf-8-sig") as f:
        return json.load(f)


COURSE_CATALOG = _load_courses()


def normalize_code(code: str) -> str:
    cleaned = "".join(code.strip().upper().split())
    for canonical in COURSE_CATALOG:
        if "".join(canonical.split()) == cleaned:
            return canonical
    return code.strip().upper()


def get_course_info(code: str):
    canonical = normalize_code(code)
    return COURSE_CATALOG.get(canonical)


def get_prerequisites(code: str):
    info = get_course_info(code)
    return info.get("prerequisites", []) if info else []


def check_prerequisites(code: str, completed_courses: list[str]):
    prereqs = get_prerequisites(code)
    completed_norm = {normalize_code(c) for c in completed_courses}
    missing = [p for p in prereqs if normalize_code(p) not in completed_norm]
    return {
        "can_take": len(missing) == 0,
        "prerequisites": prereqs,
        "missing": missing,
    }


def list_courses():
    return COURSE_CATALOG

