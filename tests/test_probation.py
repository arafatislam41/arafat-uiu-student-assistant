import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from probation import check_probation_status, check_waiver_eligibility


def test_probation_under_minimum():
    res = check_probation_status(1.85)
    assert res["is_on_probation"] is True
    assert res["status"] == "ON PROBATION"


def test_probation_good_standing():
    res = check_probation_status(2.50)
    assert res["is_on_probation"] is False
    assert res["status"] == "GOOD STANDING"


def test_waiver_100():
    res = check_waiver_eligibility(3.95)
    assert res["eligible"] is True
    assert res["percentage"] == 100


def test_waiver_50():
    res = check_waiver_eligibility(3.82)
    assert res["eligible"] is True
    assert res["percentage"] == 50


def test_waiver_25():
    res = check_waiver_eligibility(3.72)
    assert res["eligible"] is True
    assert res["percentage"] == 25


def test_waiver_ineligible():
    res = check_waiver_eligibility(3.65)
    assert res["eligible"] is False
    assert res["percentage"] == 0
