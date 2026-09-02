import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from courses import normalize_code, get_course_info, check_prerequisites


def test_normalize_code():
    assert normalize_code("cse1111") == "CSE 1111"
    assert normalize_code(" CSE  2213 ") == "CSE 2213"


def test_course_lookup():
    info = get_course_info("CSE 1111")
    assert info is not None
    assert info["credits"] == 3.0
    assert "Structured Programming" in info["title"]


def test_prerequisites_satisfied():
    # Algorithms (CSE 2215) requires Data Structures (CSE 2213)
    result = check_prerequisites("CSE 2215", ["CSE 2213"])
    assert result["can_take"] is True
    assert len(result["missing"]) == 0


def test_prerequisites_missing():
    result = check_prerequisites("CSE 2215", ["MATH 1151"])
    assert result["can_take"] is False
    assert "CSE 2213" in result["missing"]
