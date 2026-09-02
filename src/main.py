from grades import list_grades, get_grade_point, get_marks_range
from cgpa import (
    CourseResult,
    calculate_gpa,
    calculate_cgpa,
    calculate_target_cgpa,
    can_reach_target_cgpa,
)


def print_header(title):
    print()
    print("=" * 55)
    print(f"  {title}")
    print("=" * 55)


def input_number(prompt, minimum=None):
    while True:
        try:
            value = float(input(prompt).strip())

            if minimum is not None and value < minimum:
                print(f"Please enter a value >= {minimum}.")
                continue

            return value

        except ValueError:
            print("Invalid number. Please try again.")


def input_grade(prompt="Enter grade: "):
    valid_grades = list_grades()

    while True:
        grade = input(prompt).strip().upper()

        if grade in valid_grades:
            return grade

        print("Invalid grade.")
        print("Valid grades:", ", ".join(valid_grades))


def input_course():
    """Collect one course record from the user."""

    course_code = input("Course code: ").strip().upper()

    while not course_code:
        print("Course code cannot be empty.")
        course_code = input("Course code: ").strip().upper()

    grade = input_grade("Grade: ")
    credits = input_number("Credit: ", minimum=0.01)

    return CourseResult(
        course_code=course_code,
        grade=grade,
        credits=credits,
    )


def input_retake():
    """Collect one retake record: course, credits, old grade, new grade."""

    course_code = input("Course code: ").strip().upper()

    while not course_code:
        print("Course code cannot be empty.")
        course_code = input("Course code: ").strip().upper()

    credits = input_number("Credit: ", minimum=0.01)
    old_grade = input_grade("Old Grade: ")
    new_grade = input_grade("New Grade: ")

    return {
        "course_code": course_code,
        "credits": credits,
        "old_grade": old_grade,
        "new_grade": new_grade,
    }


def calculate_gpa_menu():
    print_header("GPA CALCULATOR")

    courses = []

    count = int(input_number("How many courses? ", minimum=1))

    for i in range(1, count + 1):
        print(f"\nCourse {i}")
        courses.append(input_course())

    gpa = calculate_gpa(courses)

    print()
    print("-" * 55)
    print(f"GPA: {gpa:.2f}")
    print("-" * 55)


def calculate_cgpa_menu():
    print_header("CGPA CALCULATOR")

    courses = []

    count = int(input_number("How many courses/records? ", minimum=1))

    for i in range(1, count + 1):
        print(f"\nCourse {i}")
        courses.append(input_course())

    cgpa = calculate_cgpa(courses)

    print()
    print("-" * 55)
    print(f"CGPA: {cgpa:.2f}")
    print("-" * 55)


def target_cgpa_menu():
    print_header("TARGET CGPA PLANNER")

    current_cgpa = input_number(
        "Current CGPA: ",
        minimum=0,
    )

    completed_credits = input_number(
        "Completed credits: ",
        minimum=0,
    )

    future_credits = input_number(
        "Future credits you will take: ",
        minimum=0.01,
    )

    target_cgpa = input_number(
        "Target CGPA: ",
        minimum=0,
    )

    required_gpa = calculate_target_cgpa(
        current_cgpa=current_cgpa,
        current_credits=completed_credits,
        target_cgpa=target_cgpa,
        future_credits=future_credits,
    )

    reachable = can_reach_target_cgpa(
        current_cgpa=current_cgpa,
        current_credits=completed_credits,
        target_cgpa=target_cgpa,
        future_credits=future_credits,
    )

    print()
    print("-" * 55)

    if required_gpa <= 0:
        print("Target CGPA is already achievable.")

    else:
        print(f"Required future GPA: {required_gpa:.2f}")

    if reachable:
        print("Status: TARGET IS MATHEMATICALLY REACHABLE")
    else:
        print("Status: TARGET IS NOT REACHABLE")
        print("You would need a future GPA above 4.00.")

    print("-" * 55)


def what_if_simulator_menu():
    print_header("WHAT-IF SIMULATOR")

    current_cgpa = input_number("Current CGPA: ", minimum=0)
    current_credits = input_number("Current completed credits: ", minimum=0)

    count = int(input_number("How many future courses? ", minimum=1))

    courses = []

    for i in range(1, count + 1):
        print(f"\nFuture Course {i}")
        courses.append(input_course())

    future_gpa = calculate_gpa(courses)
    future_credits = sum(course.credits for course in courses)

    total_credits = current_credits + future_credits

    if total_credits <= 0:
        new_cgpa = 0.0
    else:
        new_cgpa = (
            (current_cgpa * current_credits) + (future_gpa * future_credits)
        ) / total_credits

    target_cgpa = input_number(
        "Target CGPA (enter 0 to skip check): ",
        minimum=0,
    )

    print()
    print("-" * 55)
    print("Scenario")
    print("-" * 55)

    for i, course in enumerate(courses, start=1):
        print(f"Course {i} ({course.course_code}) -> {course.grade}")

    print()
    print(f"{'Current CGPA':<18}: {current_cgpa:.2f}")
    print(f"{'Current Credits':<18}: {current_credits:.2f}")
    print(f"{'Future Credits':<18}: {future_credits:.2f}")
    print(f"{'Future GPA':<18}: {future_gpa:.2f}")
    print(f"{'New CGPA':<18}: {new_cgpa:.2f}")

    if target_cgpa > 0:
        status = "REACHED" if new_cgpa >= target_cgpa else "NOT REACHED"
        symbol = "✓" if new_cgpa >= target_cgpa else "✗"
        print(f"{'Target ' + format(target_cgpa, '.2f'):<18}: {symbol} {status}")

    print("-" * 55)


def retake_impact_menu():
    print_header("RETAKE IMPACT CALCULATOR")

    current_cgpa = input_number("Current CGPA: ", minimum=0)
    current_credits = input_number("Current total credits: ", minimum=0.01)

    count = int(input_number("How many courses are you retaking? ", minimum=1))

    retakes = []

    for i in range(1, count + 1):
        print(f"\nRetake {i}")
        retakes.append(input_retake())

    old_total_points = current_cgpa * current_credits

    old_points_removed = sum(
        get_grade_point(r["old_grade"]) * r["credits"] for r in retakes
    )
    new_points_added = sum(
        get_grade_point(r["new_grade"]) * r["credits"] for r in retakes
    )

    new_total_points = old_total_points - old_points_removed + new_points_added
    new_cgpa = new_total_points / current_credits

    change = new_cgpa - current_cgpa

    print()
    print("-" * 55)
    print("Retake Summary")
    print("-" * 55)

    for r in retakes:
        print(
            f"{r['course_code']} ({r['credits']:.2f} cr): "
            f"{r['old_grade']} -> {r['new_grade']}"
        )

    print()
    print(f"{'Old CGPA':<18}: {current_cgpa:.2f}")
    print(f"{'New CGPA':<18}: {new_cgpa:.2f}")

    if change > 0:
        print(f"{'Change':<18}: +{change:.2f} (improved)")
    elif change < 0:
        print(f"{'Change':<18}: {change:.2f} (dropped)")
    else:
        print(f"{'Change':<18}: 0.00 (no change)")

    print("-" * 55)


def show_grade_scale():
    print_header("UIU GRADE SCALE")

    print(f"{'Grade':<8}{'Point':<10}{'Marks'}")
    print("-" * 35)

    for grade in list_grades():
        point = get_grade_point(grade)
        marks = get_marks_range(grade)

        print(f"{grade:<8}{point:<10.2f}{marks}")


def main():
    while True:
        print_header("UIU STUDENT ASSISTANT")

        print("1. Calculate GPA")
        print("2. Calculate CGPA")
        print("3. Target CGPA Planner")
        print("4. View Grade Scale")
        print("5. What-if Simulator")
        print("6. Retake Impact Calculator")
        print("0. Exit")

        print()

        choice = input("Select an option: ").strip()

        try:
            if choice == "1":
                calculate_gpa_menu()

            elif choice == "2":
                calculate_cgpa_menu()

            elif choice == "3":
                target_cgpa_menu()

            elif choice == "4":
                show_grade_scale()

            elif choice == "5":
                what_if_simulator_menu()

            elif choice == "6":
                retake_impact_menu()

            elif choice == "0":
                print("\nThank you for using UIU Student Assistant.")
                break

            else:
                print("\nInvalid option. Please select 0-6.")

        except Exception as error:
            print()
            print(f"Error: {error}")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
