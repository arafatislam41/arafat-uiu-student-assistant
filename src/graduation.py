import json
from pathlib import Path
from grades import get_marks_range

PROGRAMS_FILE = Path(__file__).resolve().parent.parent / "data" / "programs.json"


def check_degree_progress(completed_credits: float, program: str = "CSE") -> dict:
    if not PROGRAMS_FILE.exists():
        total_req = 140.0
    else:
        with open(PROGRAMS_FILE, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
            total_req = data.get(program, {}).get("total_credits_required", 140.0)

    remaining = max(0.0, total_req - completed_credits)
    progress_pct = min(100.0, (completed_credits / total_req) * 100) if total_req > 0 else 0.0

    return {
        "program": program,
        "total_required": total_req,
        "completed": completed_credits,
        "remaining": remaining,
        "progress_percentage": progress_pct,
        "is_graduated": remaining == 0.0
    }


def calculate_final_exam_target(attendance: float, quiz_assignment: float, midterm: float, target_grade: str) -> dict:
    # Standard UIU Distribution: Attendance (5), Quiz/Assign (25), Midterm (30), Final (40)
    current_obtained = attendance + quiz_assignment + midterm
    marks_range_str = get_marks_range(target_grade)
    min_required_total = float(marks_range_str.split("-")[0])

    needed_in_final = min_required_total - current_obtained

    possible = True
    impossible_reason = ""

    if needed_in_final > 40.0:
        possible = False
        impossible_reason = f"Need {needed_in_final:.1f}/40 in Final (Maximum possible is 40)"
    elif needed_in_final <= 0:
        needed_in_final = 0.0

    return {
        "target_grade": target_grade,
        "min_total_required": min_required_total,
        "current_total": current_obtained,
        "needed_in_final": needed_in_final,
        "is_achievable": possible,
        "reason": impossible_reason
    }
