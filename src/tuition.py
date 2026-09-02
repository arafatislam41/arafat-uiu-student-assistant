import json
from pathlib import Path

FEES_FILE = Path(__file__).resolve().parent.parent / "data" / "fees.json"
PROGRAMS_FILE = Path(__file__).resolve().parent.parent / "data" / "programs.json"


def _load_json(file_path):
    if not file_path.exists():
        return {}
    with open(file_path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def calculate_tuition(credits: float, waiver_percentage: float = 0.0) -> dict:
    fees = _load_json(FEES_FILE)
    cost_per_credit = fees.get("cost_per_credit", 6500.0)
    trimester_fee = fees.get("trimester_fee", 6000.0)

    gross_tuition = credits * cost_per_credit
    discount = gross_tuition * (waiver_percentage / 100.0)
    net_tuition = gross_tuition - discount
    total_payable = net_tuition + trimester_fee

    return {
        "credits": credits,
        "cost_per_credit": cost_per_credit,
        "gross_tuition": gross_tuition,
        "waiver_percentage": waiver_percentage,
        "discount": discount,
        "trimester_fee": trimester_fee,
        "total_payable": total_payable,
    }


def calculate_installments(total_payable: float) -> list[dict]:
    programs = _load_json(PROGRAMS_FILE)
    inst_rules = programs.get("installments", {})

    r1 = inst_rules.get("installment_1_ratio", 0.40)
    r2 = inst_rules.get("installment_2_ratio", 0.30)
    r3 = inst_rules.get("installment_3_ratio", 0.30)

    return [
        {
            "installment_no": 1,
            "percentage": int(r1 * 100),
            "amount": total_payable * r1,
            "deadline": inst_rules.get("installment_1_note", "At Registration")
        },
        {
            "installment_no": 2,
            "percentage": int(r2 * 100),
            "amount": total_payable * r2,
            "deadline": inst_rules.get("installment_2_note", "Before Midterm")
        },
        {
            "installment_no": 3,
            "percentage": int(r3 * 100),
            "amount": total_payable * r3,
            "deadline": inst_rules.get("installment_3_note", "Before Final")
        }
    ]
