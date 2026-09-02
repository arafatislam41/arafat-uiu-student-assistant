import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from main import (
    calculate_gpa_menu,
    target_cgpa_menu,
    what_if_simulator_menu,
    retake_impact_menu,
    show_grade_scale,
)


def run_with_inputs(func, inputs, capsys):
    """Run a menu function with a scripted sequence of input() answers."""
    with patch("builtins.input", side_effect=inputs):
        func()
    return capsys.readouterr().out


def test_calculate_gpa_menu(capsys):
    inputs = [
        "3",
        "CSE1111", "A", "3",
        "CSE2215", "B+", "3",
        "CSE2213", "B", "3",
    ]
    output = run_with_inputs(calculate_gpa_menu, inputs, capsys)
    assert "GPA: 3.44" in output


def test_target_cgpa_menu_reachable(capsys):
    inputs = ["1.85", "30", "15", "2.00"]
    output = run_with_inputs(target_cgpa_menu, inputs, capsys)
    assert "Required future GPA: 2.30" in output
    assert "TARGET IS MATHEMATICALLY REACHABLE" in output


def test_target_cgpa_menu_unreachable(capsys):
    inputs = ["0.50", "10", "3", "3.90"]
    output = run_with_inputs(target_cgpa_menu, inputs, capsys)
    assert "TARGET IS NOT REACHABLE" in output


def test_what_if_simulator_menu(capsys):
    inputs = [
        "1.85", "30",
        "5",
        "C1", "A", "3",
        "C2", "B+", "3",
        "C3", "B", "3",
        "C4", "C+", "3",
        "C5", "C", "3",
        "2.00",
    ]
    output = run_with_inputs(what_if_simulator_menu, inputs, capsys)
    assert "New CGPA" in output
    assert "REACHED" in output


def test_retake_impact_menu_improves_cgpa(capsys):
    inputs = [
        "1.85", "30",
        "1",
        "CSE1111", "3", "F", "A",
    ]
    output = run_with_inputs(retake_impact_menu, inputs, capsys)
    assert "New CGPA          : 2.25" in output
    assert "improved" in output


def test_show_grade_scale(capsys):
    with patch("builtins.input", side_effect=[]):
        show_grade_scale()
    output = capsys.readouterr().out
    assert "UIU GRADE SCALE" in output
    assert "A" in output
    assert "F" in output
