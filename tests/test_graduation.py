import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from graduation import check_degree_progress, calculate_final_exam_target, get_available_departments
from tuition import calculate_installments, calculate_tuition


def test_get_available_departments():
    depts = get_available_departments()
    assert "CSE" in depts
    assert "BBA" in depts
    assert "EEE" in depts


def test_degree_progress_cse():
    res = check_degree_progress(70.0, "CSE")
    assert res["total_required"] == 140.0
    assert res["remaining"] == 70.0
    assert res["progress_percentage"] == 50.0


def test_degree_progress_bba():
    res = check_degree_progress(63.0, "BBA")
    assert res["total_required"] == 126.0
    assert res["remaining"] == 63.0
    assert res["progress_percentage"] == 50.0


def test_tuition_rates_by_dept():
    cse_tuition = calculate_tuition(10.0, 0.0, "CSE")
    bba_tuition = calculate_tuition(10.0, 0.0, "BBA")
    assert cse_tuition["cost_per_credit"] == 6500.0
    assert bba_tuition["cost_per_credit"] == 6200.0


def test_installments_split():
    inst = calculate_installments(60000.0)
    assert len(inst) == 3
    assert inst[0]["amount"] == 24000.0
    assert inst[1]["amount"] == 18000.0
    assert inst[2]["amount"] == 18000.0


def test_final_target_achievable():
    res = calculate_final_exam_target(5, 20, 25, "A")
    assert res["is_achievable"] is True
    assert res["needed_in_final"] == 40.0


def test_final_target_impossible():
    res = calculate_final_exam_target(3, 10, 15, "A")
    assert res["is_achievable"] is False
