import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest

from cgpa import (
    CourseResult,
    calculate_gpa,
    calculate_cgpa,
    calculate_earned_credits,
    calculate_attempted_credits,
    calculate_target_cgpa,
    can_reach_target_cgpa,
    CGPAError,
)


def test_single_course_gpa():
    courses = [
        CourseResult("CSE1111", 3, "A")
    ]

    assert calculate_gpa(courses) == 4.00


def test_weighted_gpa():
    courses = [
        CourseResult("CSE1111", 3, "A"),
        CourseResult("CSE1112", 1, "B"),
    ]

    # (3×4 + 1×3) / 4 = 3.75
    assert calculate_gpa(courses) == 3.75


def test_cgpa():
    courses = [
        CourseResult("CSE1111", 3, "A"),
        CourseResult("CSE1112", 1, "B"),
        CourseResult("CSE2213", 3, "C"),
    ]

    expected = round(
        (3 * 4.00 + 1 * 3.00 + 3 * 2.00) / 7,
        2,
    )

    assert calculate_cgpa(courses) == expected


def test_f_does_not_earn_credit():
    courses = [
        CourseResult("CSE1111", 3, "F"),
        CourseResult("CSE1112", 1, "A"),
    ]

    assert calculate_earned_credits(courses) == 1.00


def test_attempted_credits():
    courses = [
        CourseResult("CSE1111", 3, "F"),
        CourseResult("CSE1112", 1, "A"),
    ]

    assert calculate_attempted_credits(courses) == 4.00


def test_target_cgpa():
    required = calculate_target_cgpa(
        current_cgpa=1.85,
        current_credits=30,
        target_cgpa=2.00,
        future_credits=15,
    )

    assert required == 2.30


def test_target_cgpa_reachable():
    assert can_reach_target_cgpa(
        current_cgpa=1.85,
        current_credits=30,
        target_cgpa=2.00,
        future_credits=15,
    ) is True


def test_target_cgpa_unreachable():
    assert can_reach_target_cgpa(
        current_cgpa=1.00,
        current_credits=100,
        target_cgpa=3.50,
        future_credits=10,
    ) is False


def test_empty_course_list():
    with pytest.raises(CGPAError):
        calculate_gpa([])


def test_invalid_credits():
    with pytest.raises(CGPAError):
        CourseResult("CSE1111", 0, "A")