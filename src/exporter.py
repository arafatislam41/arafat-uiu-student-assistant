import csv
from pathlib import Path
from datetime import datetime
from config import get_user_data_dir


def export_schedule_csv(courses: list[dict], filename: str = "uiu_routine_schedule.csv") -> Path:
    """Exports routine courses to a CSV spreadsheet."""
    export_dir = get_user_data_dir() / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)
    file_path = export_dir / filename

    with open(file_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Course Code", "Section", "Days", "Time Slot"])
        for c in courses:
            writer.writerow([
                c.get("code", ""),
                c.get("section", ""),
                c.get("days", ""),
                c.get("time", "")
            ])

    return file_path


def export_academic_summary_html(profile: dict, tuition: dict, installments: list[dict], filename: str = "uiu_academic_statement.html") -> Path:
    """Exports a stylized, printable academic statement in UIU branding."""
    export_dir = get_user_data_dir() / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)
    file_path = export_dir / filename

    now = datetime.now().strftime("%d %b %Y, %I:%M %p")

    inst_rows = "".join([
        f"<tr><td>Installment {i['installment_no']} ({i['percentage']}%)</td><td><strong>{i['amount']:,.2f} BDT</strong></td><td>{i['deadline']}</td></tr>"
        for i in installments
    ])

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>UIU Student Academic Statement</title>
<style>
  body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background: #fafafa; color: #222; }}
  .card {{ background: #fff; max-width: 800px; margin: auto; padding: 35px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); border-top: 6px solid #F26522; }}
  .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #eee; padding-bottom: 15px; }}
  .badge {{ background: #F26522; color: #fff; font-size: 26px; font-weight: bold; padding: 6px 16px; border-radius: 6px; }}
  .title {{ font-size: 20px; font-weight: bold; color: #171F2A; }}
  .meta {{ margin-top: 20px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 14px; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 25px; }}
  th, td {{ border: 1px solid #ddd; padding: 10px 14px; text-align: left; font-size: 14px; }}
  th {{ background: #171F2A; color: white; }}
  .total-row {{ background: #FFF4EE; font-weight: bold; font-size: 15px; color: #F26522; }}
  .footer {{ margin-top: 30px; font-size: 12px; color: #777; text-align: center; border-top: 1px solid #eee; padding-top: 12px; }}
</style>
</head>
<body>
<div class="card">
  <div class="header">
    <div>
      <div class="title">UNITED INTERNATIONAL UNIVERSITY</div>
      <div style="color: #666; font-size: 13px;">Academic & Tuition Billing Statement</div>
    </div>
    <div class="badge">UIU</div>
  </div>

  <div class="meta">
    <div><strong>Student Name:</strong> {profile.get('name', 'N/A')}</div>
    <div><strong>Student ID:</strong> {profile.get('student_id', 'N/A')}</div>
    <div><strong>Department:</strong> {tuition.get('department', 'N/A')}</div>
    <div><strong>CGPA:</strong> {profile.get('current_cgpa', 0.0):.2f}</div>
  </div>

  <h3 style="margin-top: 25px; color: #171F2A; border-bottom: 2px solid #F26522; display: inline-block; padding-bottom: 3px;">Trimester Tuition Breakdown</h3>
  <table>
    <tr><th>Item Description</th><th>Rate / Basis</th><th>Amount (BDT)</th></tr>
    <tr><td>Tuition Fee ({tuition.get('credits', 0.0):.1f} Credits)</td><td>{tuition.get('cost_per_credit', 0.0):,.2f} BDT/cr</td><td>{tuition.get('gross_tuition', 0.0):,.2f}</td></tr>
    <tr><td>Merit Waiver Discount ({int(tuition.get('waiver_percentage', 0))}%)</td><td>Special Policy</td><td style="color: green;">-{tuition.get('discount', 0.0):,.2f}</td></tr>
    <tr><td>Trimester Activities & Lab Fee</td><td>Flat Rate</td><td>+{tuition.get('trimester_fee', 0.0):,.2f}</td></tr>
    <tr class="total-row"><td>Total Net Payable</td><td>-</td><td>{tuition.get('total_payable', 0.0):,.2f} BDT</td></tr>
  </table>

  <h3 style="margin-top: 25px; color: #171F2A; border-bottom: 2px solid #F26522; display: inline-block; padding-bottom: 3px;">3-Installment Payment Deadlines</h3>
  <table>
    <tr><th>Installment</th><th>Payable Amount</th><th>Deadline Notice</th></tr>
    {inst_rows}
  </table>

  <div class="footer">
    Generated via UIU Student Assistant V2 on {now}. Keep this document for reference.
  </div>
</div>
</body>
</html>
"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return file_path
