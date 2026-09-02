from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from grades import get_grade_point, is_earned_credit_grade


class CGPAError(ValueError):
    """Raised when invalid CGPA/GPA data is supplied."""


@dataclass(frozen=True)
class CourseResult:
    """
    Represents one completed course result.

    Example:
        CourseResult("CSE1111", 3, "B+")
    """

    course_code: str
    credits: float
    grade: str

    def __post_init__(self) -> None:
        if not self.course_code or not self.course_code.strip():
            raise CGPAError("Course code cannot be empty.")

        if self.credits <= 0:
            raise CGPAError("Course credits must be greater than zero.")

        # Validate the grade immediately.
        get_grade_point(self.grade)

    @property
    def grade_point(self) -> float:
        return get_grade_point(self.grade)

    @property
    def quality_points(self) -> float:
        return self.credits * self.grade_point

    @property
    def earned_credits(self) -> float:
        if is_earned_credit_grade(self.grade):
            return self.credits

        return 0.0


def calculate_gpa(courses: Iterable[CourseResult]) -> float:
    """
    Calculate credit-weighted GPA.

    GPA = Σ(credit × grade point) / Σ(credits)
    """
    courses = list(courses)

    if not courses:
        raise CGPAError("At least one course is required.")

    total_quality_points = sum(
        course.quality_points for course in courses
    )

    total_credits = sum(
        course.credits for course in courses
    )

    if total_credits <= 0:
        raise CGPAError("Total credits must be greater than zero.")

    return round(total_quality_points / total_credits, 2)


def calculate_earned_credits(
    courses: Iterable[CourseResult],
) -> float:
    """Calculate credits earned from D or higher."""
    return round(
        sum(course.earned_credits for course in courses),
        2,
    )


def calculate_attempted_credits(
    courses: Iterable[CourseResult],
) -> float:
    """Calculate total credits attempted."""
    return round(
        sum(course.credits for course in courses),
        2,
    )


def calculate_cgpa(
    courses: Iterable[CourseResult],
) -> float:
    """
    Calculate cumulative CGPA from all supplied course results.

    For the current engine, each supplied result participates
    in the credit-weighted calculation.
    """
    return calculate_gpa(courses)


def calculate_target_cgpa(
    current_cgpa: float,
    current_credits: float,
    target_cgpa: float,
    future_credits: float,
) -> float:
    """
    Calculate the GPA required in future credits to reach a target CGPA.

    Required GPA =
        ((target CGPA × (current credits + future credits))
        - (current CGPA × current credits))
        / future credits
    """

    if current_cgpa < 0 or current_cgpa > 4:
        raise CGPAError("Current CGPA must be between 0 and 4.")

    if target_cgpa < 0 or target_cgpa > 4:
        raise CGPAError("Target CGPA must be between 0 and 4.")

    if current_credits < 0:
        raise CGPAError("Current credits cannot be negative.")

    if future_credits <= 0:
        raise CGPAError("Future credits must be greater than zero.")

    required_gpa = (
        (
            target_cgpa
            * (current_credits + future_credits)
        )
        - (current_cgpa * current_credits)
    ) / future_credits

    return round(required_gpa, 2)


def can_reach_target_cgpa(
    current_cgpa: float,
    current_credits: float,
    target_cgpa: float,
    future_credits: float,
) -> bool:
    """
    Determine whether the target CGPA is mathematically reachable
    with a maximum future GPA of 4.00.
    """
    required_gpa = calculate_target_cgpa(
        current_cgpa=current_cgpa,
        current_credits=current_credits,
        target_cgpa=target_cgpa,
        future_credits=future_credits,
    )

    return required_gpa <= 4.00