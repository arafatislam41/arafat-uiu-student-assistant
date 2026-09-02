import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "policies.json"


def _load_policies():
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, "r", encoding="utf-8-sig") as f:
        return json.load(f)


POLICIES = _load_policies()


def check_probation_status(cgpa: float) -> dict:
    probation_cfg = POLICIES.get("probation", {})
    min_cgpa = probation_cfg.get("minimum_cgpa", 2.00)
    is_on_probation = cgpa < min_cgpa

    return {
        "is_on_probation": is_on_probation,
        "cgpa": cgpa,
        "status": "ON PROBATION" if is_on_probation else "GOOD STANDING",
        "message": probation_cfg.get("warning_message") if is_on_probation else probation_cfg.get("good_standing_message")
    }


def check_waiver_eligibility(cgpa: float) -> dict:
    slabs = POLICIES.get("waiver_slabs", [])
    for slab in slabs:
        if cgpa >= slab["min_cgpa"]:
            return {
                "eligible": True,
                "percentage": slab["waiver_percentage"],
                "remarks": slab["remarks"]
            }
    return {
        "eligible": False,
        "percentage": 0,
        "remarks": "No merit waiver applicable (Requires CGPA >= 3.70)"
    }
