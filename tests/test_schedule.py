import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from schedule import check_schedule_conflicts, parse_slot_time_range, normalize_days


def test_time_parsing():
    start, end = parse_slot_time_range("08:30 - 10:00")
    assert start == 510  # 8*60 + 30
    assert end == 600    # 10*60


def test_days_normalization():
    days_st = normalize_days("ST")
    assert "SUN" in days_st and "TUE" in days_st
    days_mw = normalize_days("MW")
    assert "MON" in days_mw and "WED" in days_mw


def test_no_conflict():
    slots = [
        {"code": "CSE 1111", "section": "A", "days": "ST", "time": "08:30 - 10:00"},
        {"code": "CSE 1112", "section": "B", "days": "ST", "time": "10:05 - 11:35"},
        {"code": "MATH 1151", "section": "C", "days": "MW", "time": "08:30 - 10:00"}
    ]
    res = check_schedule_conflicts(slots)
    assert res["has_conflict"] is False
    assert len(res["conflicts"]) == 0


def test_time_conflict_detected():
    # Both on ST, overlapping between 09:30 and 10:00 (30 mins)
    slots = [
        {"code": "CSE 2213", "section": "A", "days": "ST", "time": "08:30 - 10:00"},
        {"code": "CSE 2215", "section": "B", "days": "ST", "time": "09:30 - 11:00"}
    ]
    res = check_schedule_conflicts(slots)
    assert res["has_conflict"] is True
    assert res["conflict_count"] == 1
    assert res["conflicts"][0]["overlap_minutes"] == 30
