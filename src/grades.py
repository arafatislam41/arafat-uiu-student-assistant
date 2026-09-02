import json
from pathlib import Path


class GradeError(ValueError):
    """Raised when an invalid grade is supplied."""


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "grading.json"


def _load_grading_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


GRADING_DATA = _load_grading_data()


def normalize_grade(grade):
    """Normalize grade input."""
    if not isinstance(grade, str):
        raise GradeError("Grade must be a string.")

    return grade.strip().upper()


def _validate_grade(grade):
    grade = normalize_grade(grade)

    if grade not in GRADING_DATA:
        raise GradeError(f"Invalid grade: {grade}")

    return grade


def get_all_grades():
    """Return all valid UIU grades."""
    return list(GRADING_DATA.keys())


def list_grades():
    """Alias for get_all_grades()."""
    return get_all_grades()


def get_grade_point(grade):
    """Return grade point for a grade."""
    grade = _validate_grade(grade)
    return float(GRADING_DATA[grade]["point"])


def get_grade_marks(grade):
    """Return marks range for a grade."""
    grade = _validate_grade(grade)
    return GRADING_DATA[grade]["marks"]


def get_marks_range(grade):
    """Alias for get_grade_marks()."""
    return get_grade_marks(grade)


def is_passing_grade(grade):
    """Return True if the grade is passing."""
    grade = _validate_grade(grade)
    return grade != "F"


def is_passing(grade):
    """Alias for is_passing_grade()."""
    return is_passing_grade(grade)


def is_earned_credit_grade(grade):
    """Return True if the grade earns academic credit."""
    grade = _validate_grade(grade)
    return grade != "F"


def earns_credit(grade):
    """Alias for is_earned_credit_grade()."""
    return is_earned_credit_grade(grade)


def get_grade_info(grade):
    """Return complete information about a grade."""
    grade = _validate_grade(grade)

    return {
        "grade": grade,
        "point": float(GRADING_DATA[grade]["point"]),
        "marks": GRADING_DATA[grade]["marks"],
        "passing": is_passing_grade(grade),
        "earns_credit": is_earned_credit_grade(grade),
    }
