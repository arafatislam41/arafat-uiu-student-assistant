import re
from datetime import datetime


def _parse_time_to_minutes(time_str: str) -> int:
    """Converts '08:30 AM' or '08:30' or '2:15 PM' into minutes from midnight."""
    time_str = time_str.strip().upper()
    
    # Check if 12-hour format with AM/PM
    match_12 = re.match(r"^(\d{1,2}):(\d{2})\s*(AM|PM)$", time_str)
    if match_12:
        hr, mn, period = match_12.groups()
        hr = int(hr)
        mn = int(mn)
        if period == "PM" and hr != 12:
            hr += 12
        elif period == "AM" and hr == 12:
            hr = 0
        return (hr * 60) + mn

    # 24-hour fallback format 'HH:MM'
    match_24 = re.match(r"^(\d{1,2}):(\d{2})$", time_str)
    if match_24:
        hr, mn = match_24.groups()
        return (int(hr) * 60) + int(mn)

    raise ValueError(f"Invalid time format: '{time_str}'. Use HH:MM or HH:MM AM/PM.")


def parse_slot_time_range(time_range_str: str) -> tuple[int, int]:
    """Parses '08:30 - 10:00' or '08:30 AM - 10:00 AM' into (start_min, end_min)."""
    parts = time_range_str.split("-")
    if len(parts) != 2:
        raise ValueError(f"Invalid time range: '{time_range_str}'. Format should be 'Start - End'.")

    start_min = _parse_time_to_minutes(parts[0].strip())
    end_min = _parse_time_to_minutes(parts[1].strip())

    if end_min <= start_min:
        raise ValueError(f"End time must be after start time in '{time_range_str}'.")

    return start_min, end_min


def normalize_days(days_str: str) -> list[str]:
    """
    Normalizes UIU day codes:
    ST -> Sunday, Tuesday
    MW -> Monday, Wednesday
    RA -> Thursday, Saturday
    Or individual day abbreviations: SUN, MON, TUE, WED, THU, FRI, SAT.
    """
    cleaned = days_str.strip().upper().replace(" ", "").replace("/", "").replace(",", "")
    day_map = {
        "ST": ["SUN", "TUE"],
        "MW": ["MON", "WED"],
        "RA": ["THU", "SAT"],
        "SR": ["SUN", "THU"],
    }
    if cleaned in day_map:
        return day_map[cleaned]

    # Individual day matching
    tokens = re.findall(r"(SUN|MON|TUE|WED|THU|FRI|SAT|S|M|T|W|R|A)", cleaned)
    short_map = {"S": "SUN", "M": "MON", "T": "TUE", "W": "WED", "R": "THU", "A": "SAT"}
    normalized = []
    for t in tokens:
        normalized.append(short_map.get(t, t))
    return list(set(normalized)) if normalized else [cleaned]


def check_schedule_conflicts(courses: list[dict]) -> dict:
    """
    Takes a list of course slot dicts:
    [
      {"code": "CSE 2213", "section": "A", "days": "ST", "time": "08:30 - 10:00"},
      {"code": "CSE 2215", "section": "B", "days": "ST", "time": "09:30 - 11:00"}
    ]
    Returns conflict status and detailed clashes if any.
    """
    conflicts = []
    parsed_slots = []

    for idx, c in enumerate(courses):
        try:
            days = normalize_days(c.get("days", ""))
            start_m, end_m = parse_slot_time_range(c.get("time", ""))
            parsed_slots.append({
                "index": idx,
                "code": c.get("code", f"Course {idx+1}").strip().upper(),
                "section": c.get("section", "").strip().upper(),
                "days": days,
                "start": start_m,
                "end": end_m,
                "time_str": c.get("time", "")
            })
        except Exception as e:
            return {"has_conflict": True, "error": str(e), "conflicts": []}

    # Pairwise overlap detection
    for i in range(len(parsed_slots)):
        for j in range(i + 1, len(parsed_slots)):
            s1 = parsed_slots[i]
            s2 = parsed_slots[j]

            # Check shared day
            shared_days = set(s1["days"]).intersection(set(s2["days"]))
            if shared_days:
                # Check time intersection: max(start1, start2) < min(end1, end2)
                overlap_start = max(s1["start"], s2["start"])
                overlap_end = min(s1["end"], s2["end"])
                if overlap_start < overlap_end:
                    conflicts.append({
                        "course_1": f"{s1['code']} [{s1['section']}] ({s1['time_str']})",
                        "course_2": f"{s2['code']} [{s2['section']}] ({s2['time_str']})",
                        "clashing_days": list(shared_days),
                        "overlap_minutes": overlap_end - overlap_start
                    })

    return {
        "has_conflict": len(conflicts) > 0,
        "conflict_count": len(conflicts),
        "conflicts": conflicts
    }
