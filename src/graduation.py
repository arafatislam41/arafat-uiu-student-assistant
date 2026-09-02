import json
import re
from grades import get_marks_range
from config import get_data_dir

PROGRAMS_FILE = get_data_dir() / "programs.json"


def _load_programs():
    if not PROGRAMS_FILE.exists():
        return {}
    with open(PROGRAMS_FILE, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def get_available_departments() -> list[str]:
    data = _load_programs()
    return list(data.get("departments", {}).keys())


def get_department_info(dept_code: str) -> dict:
    data = _load_programs()
    depts = data.get("departments", {})
    return depts.get(dept_code.upper(), {
        "name": f"Department of {dept_code}",
        "faculty": "General Program",
        "total_credits": 130.0,
        "cost_per_credit": 6500.0
    })


def check_degree_progress(completed_credits: float, program: str = "CSE") -> dict:
    info = get_department_info(program)
    total_req = float(info.get("total_credits", 140.0))

    remaining = max(0.0, total_req - completed_credits)
    progress_pct = min(100.0, (completed_credits / total_req) * 100) if total_req > 0 else 0.0

    return {
        "program_code": program.upper(),
        "program_name": info.get("name", program),
        "faculty": info.get("faculty", ""),
        "total_required": total_req,
        "completed": completed_credits,
        "remaining": remaining,
        "progress_percentage": progress_pct,
        "is_graduated": remaining == 0.0
    }


def calculate_final_exam_target(attendance: float, quiz_assignment: float, midterm: float, target_grade: str) -> dict:
    current_obtained = attendance + quiz_assignment + midterm
    marks_range_str = str(get_marks_range(target_grade)).strip()

    numbers = re.findall(r"\d+", marks_range_str)
    min_required_total = float(numbers[0]) if numbers else 80.0

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
