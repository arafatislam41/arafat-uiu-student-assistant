import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from examcon import save_exam_entry, get_all_exam_entries, delete_exam_entry


def test_exam_schedule_crud():
    # Insert test exam
    save_exam_entry("CSE 2213", "Midterm", "2026-10-15", "09:00 AM - 11:00 AM", "Room 412")
    records = get_all_exam_entries()
    assert len(records) >= 1
    
    latest = records[-1]
    assert latest["course_code"] == "CSE 2213"
    assert latest["room_no"] == "ROOM 412"

    # Cleanup
    delete_exam_entry(latest["id"])
    after_records = [r for r in get_all_exam_entries() if r["id"] == latest["id"]]
    assert len(after_records) == 0
