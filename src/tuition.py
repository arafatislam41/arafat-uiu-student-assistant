import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "fees.json"


def _load_fees():
    if not DATA_FILE.exists():
        return {"cost_per_credit": 6500.0, "trimester_fee": 6000.0}
    with open(DATA_FILE, "r", encoding="utf-8-sig") as f:
        return json.load(f)


FEES = _load_fees()


def calculate_tuition(credits: float, waiver_percentage: float = 0.0) -> dict:
    cost_per_credit = FEES.get("cost_per_credit", 6500.0)
    trimester_fee = FEES.get("trimester_fee", 6000.0)

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
