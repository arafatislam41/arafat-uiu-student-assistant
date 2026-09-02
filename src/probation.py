import json
from config import get_data_dir

POLICIES_FILE = get_data_dir() / "policies.json"


def _load_policies():
    if not POLICIES_FILE.exists():
        return {}
    with open(POLICIES_FILE, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def check_probation_status(cgpa: float) -> dict:
    policies = _load_policies()
    limit = policies.get("probation_limit", 2.00)
    is_probation = cgpa < limit
    return {
        "is_on_probation": is_probation,
        "status": "ON PROBATION" if is_probation else "GOOD STANDING",
        "message": (
            f"Your CGPA is below {limit:.2f}. You are currently on academic probation."
            if is_probation
            else "Your academic standing is good."
        ),
    }


def check_waiver_eligibility(cgpa: float) -> dict:
    policies = _load_policies()
    waivers = policies.get("merit_waiver_slabs", [])

    if not waivers:
        # Standard fallback slabs: 3.90+ -> 100%, 3.80+ -> 50%, 3.70+ -> 25%
        waivers = [
            {"min_cgpa": 3.90, "waiver_percentage": 100, "remarks": "100% Merit Waiver"},
            {"min_cgpa": 3.80, "waiver_percentage": 50, "remarks": "50% Merit Waiver"},
            {"min_cgpa": 3.70, "waiver_percentage": 25, "remarks": "25% Merit Waiver"}
        ]

    for w in sorted(waivers, key=lambda x: x.get("min_cgpa", x.get("min_gpa", 0.0)), reverse=True):
        min_score = w.get("min_cgpa", w.get("min_gpa", 0.0))
        if cgpa >= min_score:
            return {
                "eligible": True,
                "percentage": w.get("waiver_percentage", 0),
                "remarks": w.get("remarks", "Merit Waiver"),
            }

    return {
        "eligible": False,
        "percentage": 0,
        "remarks": "Not eligible for merit waiver.",
    }
