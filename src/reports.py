from datetime import datetime
from pathlib import Path


def generate_student_report(profile: dict, probation_info: dict, waiver_info: dict) -> Path:
    out_dir = Path(__file__).resolve().parent.parent / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    report_file = out_dir / f"report_{profile.get('student_id', 'student')}.txt"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content = f"""============================================================
              UIU STUDENT ACADEMIC SUMMARY
============================================================
Date Generated: {timestamp}

STUDENT PROFILE:
  Name             : {profile.get('name')}
  Student ID       : {profile.get('student_id')}
  Current CGPA     : {profile.get('current_cgpa'):.2f}
  Completed Credits: {profile.get('completed_credits'):.2f}

ACADEMIC STANDING:
  Status           : {probation_info.get('status')}
  Remarks          : {probation_info.get('message')}

TUITION WAIVER:
  Eligible Waiver  : {waiver_info.get('percentage')}%
  Details          : {waiver_info.get('remarks')}
============================================================
"""
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(content)

    return report_file
