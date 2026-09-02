import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "bus_routes.json"


def _load_routes():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
        return data.get("routes", [])


def get_all_routes():
    """Return all available UIU bus routes."""
    return _load_routes()


def find_routes_by_stop(query: str):
    """Search for routes that cover a specific stoppage or area."""
    query = query.strip().lower()
    if not query:
        return []
    
    matches = []
    for r in _load_routes():
        # Match by route name or pickup stops
        name_match = query in r["route_name"].lower()
        stop_match = any(query in stop.lower() for stop in r["pickup_stops"])
        if name_match or stop_match:
            matches.append(r)
    return matches
