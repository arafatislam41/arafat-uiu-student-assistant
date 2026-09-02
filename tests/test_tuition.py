import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from tuition import calculate_tuition


def test_tuition_no_waiver():
    res = calculate_tuition(9.0, 0.0)
    assert res["gross_tuition"] == 58500.0
    assert res["discount"] == 0.0
    assert res["total_payable"] == 64500.0


def test_tuition_with_waiver():
    res = calculate_tuition(9.0, 50.0)
    assert res["gross_tuition"] == 58500.0
    assert res["discount"] == 29250.0
    assert res["total_payable"] == 35250.0
