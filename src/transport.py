import json
from config import get_data_dir

DATA_FILE = get_data_dir() / "bus_routes.json"

def _load_routes():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
        return data.get("routes", [])

def get_all_routes():
    return _load_routes()

def find_routes_by_stop(query: str):
    query = query.strip().lower()
    if not query:
        return []
    matches = []
    for r in _load_routes():
        name_match = query in r["route_name"].lower()
        stop_match = any(query in stop.lower() for stop in r["pickup_stops"])
        if name_match or stop_match:
            matches.append(r)
    return matches
