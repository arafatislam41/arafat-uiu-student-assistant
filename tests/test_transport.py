import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from transport import get_all_routes, find_routes_by_stop


def test_get_all_routes():
    routes = get_all_routes()
    assert len(routes) >= 5
    route_names = [r["route_name"] for r in routes]
    assert any("Mirpur" in name for name in route_names)
    assert any("Uttara" in name for name in route_names)


def test_find_routes_by_stop_mirpur():
    matches = find_routes_by_stop("Kazipara")
    assert len(matches) == 1
    assert "Mirpur" in matches[0]["route_name"]


def test_find_routes_by_stop_notun_bazar():
    matches = find_routes_by_stop("Nadda")
    assert len(matches) == 1
    assert "Shuttle" in matches[0]["route_name"]


def test_find_routes_empty():
    assert find_routes_by_stop("Chattogram") == []
