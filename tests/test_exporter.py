import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from exporter import export_schedule_csv, export_academic_summary_html


def test_export_schedule_csv(tmp_path):
    sample_courses = [
        {"code": "CSE 2213", "section": "A", "days": "ST", "time": "08:30 - 10:00"},
        {"code": "CSE 2215", "section": "B", "days": "ST", "time": "10:05 - 11:35"}
    ]
    file_path = export_schedule_csv(sample_courses, "test_routine.csv")
    assert file_path.exists()
    content = file_path.read_text(encoding="utf-8-sig")
    assert "CSE 2213" in content
    assert "08:30 - 10:00" in content


def test_export_academic_summary_html(tmp_path):
    prof = {"name": "Test Student", "student_id": "011231999", "current_cgpa": 3.85}
    tuition = {
        "department": "CSE",
        "credits": 9.0,
        "cost_per_credit": 6500.0,
        "gross_tuition": 58500.0,
        "waiver_percentage": 50,
        "discount": 29250.0,
        "trimester_fee": 6000.0,
        "total_payable": 35250.0
    }
    installments = [
        {"installment_no": 1, "percentage": 40, "amount": 14100.0, "deadline": "At Registration"},
        {"installment_no": 2, "percentage": 30, "amount": 10575.0, "deadline": "Before Midterm"},
        {"installment_no": 3, "percentage": 30, "amount": 10575.0, "deadline": "Before Final"}
    ]
    file_path = export_academic_summary_html(prof, tuition, installments, "test_statement.html")
    assert file_path.exists()
    html = file_path.read_text(encoding="utf-8")
    assert "Test Student" in html
    assert "35,250.00 BDT" in html
