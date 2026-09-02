import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from graduation import check_degree_progress, calculate_final_exam_target
from tuition import calculate_installments


def test_degree_progress():
    res = check_degree_progress(70.0, "CSE")
    assert res["total_required"] == 140.0
    assert res["remaining"] == 70.0
    assert res["progress_percentage"] == 50.0


def test_installments_split():
    inst = calculate_installments(60000.0)
    assert len(inst) == 3
    assert inst[0]["amount"] == 24000.0  # 40%
    assert inst[1]["amount"] == 18000.0  # 30%
    assert inst[2]["amount"] == 18000.0  # 30%


def test_final_target_achievable():
    # Att: 5, Quiz: 20, Mid: 25 -> Total: 50. Target 'A' (90 min). Needed in final: 40.0 (Achievable)
    res = calculate_final_exam_target(5, 20, 25, "A")
    assert res["is_achievable"] is True
    assert res["needed_in_final"] == 40.0


def test_final_target_impossible():
    # Att: 3, Quiz: 10, Mid: 15 -> Total: 28. Target 'A' (90 min). Needed: 62 (Impossible)
    res = calculate_final_exam_target(3, 10, 15, "A")
    assert res["is_achievable"] is False
