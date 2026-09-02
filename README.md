# UIU Student Assistant

A command-line tool for UIU (United International University) students to calculate GPA, CGPA, plan target CGPA, simulate what-if scenarios, and estimate the impact of retaking courses.

## Features

1. **Calculate GPA** — Enter courses (code, grade, credit) for a single semester and get the GPA.
2. **Calculate CGPA** — Enter all courses/records across semesters and get the overall CGPA.
3. **Target CGPA Planner** — Given current CGPA, completed credits, future credits, and a target CGPA, calculates the GPA required in future courses to hit the target, and whether it's mathematically reachable.
4. **View Grade Scale** — Displays the full UIU grade scale (grade, grade point, marks range).
5. **What-if Simulator** — Given a current CGPA/credits and a set of hypothetical future course grades, calculates the resulting new CGPA, with an optional target check.
6. **Retake Impact Calculator** — Given a current CGPA/credits and one or more courses being retaken (old grade → new grade), calculates the new CGPA after the retake(s).

## UIU Grade Scale

| Grade | Point | Marks   |
|-------|-------|---------|
| A     | 4.00  | 90-100  |
| A-    | 3.67  | 86-89   |
| B+    | 3.33  | 82-85   |
| B     | 3.00  | 78-81   |
| B-    | 2.67  | 74-77   |
| C+    | 2.33  | 70-73   |
| C     | 2.00  | 66-69   |
| C-    | 1.67  | 62-65   |
| D+    | 1.33  | 58-61   |
| D     | 1.00  | 55-57   |
| F     | 0.00  | 0-54    |

## Project Structure

\\\
.
├── data/
│   └── grading.json       # Grade scale data (point + marks range per grade)
├── src/
│   ├── grades.py           # Grade validation, lookup, and info functions
│   ├── cgpa.py              # CourseResult, GPA/CGPA/target CGPA calculations
│   └── main.py              # CLI menu and all interactive menu functions
├── tests/
│   ├── test_grades.py
│   ├── test_cgpa.py
│   └── test_main.py
└── README.md
\\\

## Requirements

- Python 3.10+
- pytest (for running tests)

## Setup

\\\powershell
python -m venv .venv
.venv\Scripts\activate
pip install pytest
\\\

## Usage

\\\powershell
python src\main.py
\\\

Then choose an option from the menu (0-6).

## Running Tests

\\\powershell
python -m pytest -v
\\\

All 27 tests (grades, cgpa, and main menu functions) should pass.

## Example: What-if Simulator

\\\
Current CGPA: 1.85
Current completed credits: 30
How many future courses? 5
... (enter 5 courses with grades and credits) ...
Target CGPA (enter 0 to skip check): 2.00
\\\

Output shows the scenario, future GPA, new CGPA, and whether the target was reached.

## Example: Retake Impact Calculator

\\\
Current CGPA: 1.85
Current total credits: 30
How many courses are you retaking? 1
Course code: CSE1111
Credit: 3
Old Grade: F
New Grade: A
\\\

Output:
\\\
Old CGPA          : 1.85
New CGPA          : 2.25
Change            : +0.40 (improved)
\\\

## Roadmap

- Result history / saved records across semesters
- Course planner (schedule future semesters against target CGPA)

## Author

Md Arafat Islam — CSE, United International University (UIU)
