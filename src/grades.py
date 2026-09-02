import json
import sys
from pathlib import Path
from config import get_data_dir

DATA_FILE = get_data_dir() / "grading.json"


class GradeError(Exception):
    """Custom exception raised for invalid grades."""
    pass


def _load_grading_data():
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def list_grades():
    data = _load_grading_data()
    return list(data.keys())


def get_all_grades():
    data = _load_grading_data()
    return data


def normalize_grade(grade: str) -> str:
    return grade.strip().upper()


def is_valid_grade(grade: str) -> bool:
    return normalize_grade(grade) in list_grades()


def is_passing_grade(grade: str) -> bool:
    """Returns True if the grade is a valid passing grade (not F)."""
    norm = normalize_grade(grade)
    return is_valid_grade(norm) and norm != "F"


def is_earned_credit_grade(grade: str) -> bool:
    """Returns True if the grade earns academic credits."""
    return is_passing_grade(grade)


def get_grade_info(grade: str) -> dict:
    data = _load_grading_data()
    norm = normalize_grade(grade)
    item = data.get(norm)
    if not item:
        raise GradeError(f"Invalid grade: {grade}")
    return item


def get_grade_point(grade: str) -> float:
    info = get_grade_info(grade)
    return float(info["point"])


def get_marks_range(grade: str) -> str:
    info = get_grade_info(grade)
    return info.get("marks", "")


def get_grade_marks(grade: str) -> str:
    """Alias for get_marks_range."""
    return get_marks_range(grade)
