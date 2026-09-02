import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from grades import (
    get_grade_point,
    get_grade_marks,
    get_all_grades,
    is_passing_grade,
    is_earned_credit_grade,
    GradeError,
)


def test_a_grade():
    assert get_grade_point("A") == 4.00


def test_lowercase_grade():
    assert get_grade_point("a") == 4.00


def test_grade_with_spaces():
    assert get_grade_point(" B+ ") == 3.33


def test_f_grade():
    assert get_grade_point("F") == 0.00


def test_marks_range():
    assert get_grade_marks("A") == "90-100"


def test_d_is_passing():
    assert is_passing_grade("D") is True


def test_f_is_not_passing():
    assert is_passing_grade("F") is False


def test_d_earns_credit():
    assert is_earned_credit_grade("D") is True


def test_f_does_not_earn_credit():
    assert is_earned_credit_grade("F") is False


def test_all_grades():
    grades = get_all_grades()

    assert "A" in grades
    assert "A-" in grades
    assert "B+" in grades
    assert "F" in grades


def test_invalid_grade():
    try:
        get_grade_point("X")
        assert False
    except GradeError:
        assert True