from grades import list_grades, get_grade_point, get_marks_range
from cgpa import (
    CourseResult,
    calculate_gpa,
    calculate_cgpa,
    calculate_target_cgpa,
    can_reach_target_cgpa,
)
from profile import get_profile, update_profile
from courses import get_course_info, normalize_code, list_courses, check_prerequisites
from probation import check_probation_status, check_waiver_eligibility


def print_header(title):
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)


def input_number(prompt, minimum=None, default=None):
    prompt_text = f"{prompt} [{default}]: " if default is not None else f"{prompt}: "
    while True:
        try:
            raw = input(prompt_text).strip()
            if not raw and default is not None:
                return default
            value = float(raw)
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
    raw_code = input("Course code: ").strip().upper()
    while not raw_code:
        print("Course code cannot be empty.")
        raw_code = input("Course code: ").strip().upper()

    canonical_code = normalize_code(raw_code)
    catalog_info = get_course_info(canonical_code)

    default_credits = None
    if catalog_info:
        print(f"  -> Detected: {catalog_info['title']} ({catalog_info['credits']} cr)")
        default_credits = catalog_info["credits"]

    grade = input_grade("Grade: ")
    credits = input_number("Credit", minimum=0.01, default=default_credits)

    return CourseResult(
        course_code=canonical_code,
        grade=grade,
        credits=credits,
    )


def input_retake():
    raw_code = input("Course code: ").strip().upper()
    while not raw_code:
        print("Course code cannot be empty.")
        raw_code = input("Course code: ").strip().upper()

    canonical_code = normalize_code(raw_code)
    catalog_info = get_course_info(canonical_code)
    default_credits = catalog_info["credits"] if catalog_info else None

    if catalog_info:
        print(f"  -> Detected: {catalog_info['title']} ({catalog_info['credits']} cr)")

    credits = input_number("Credit", minimum=0.01, default=default_credits)
    old_grade = input_grade("Old Grade: ")
    new_grade = input_grade("New Grade: ")

    return {
        "course_code": canonical_code,
        "credits": credits,
        "old_grade": old_grade,
        "new_grade": new_grade,
    }


def manage_profile_menu():
    print_header("MANAGE PROFILE")
    profile = get_profile()

    print(f"Current Name: {profile['name']}")
    name = input("Enter new name (leave empty to keep current): ").strip()

    print(f"Current ID: {profile['student_id']}")
    student_id = input("Enter new ID (leave empty to keep current): ").strip()

    print(f"Current CGPA: {profile['current_cgpa']}")
    cgpa_str = input("Enter new CGPA (leave empty to keep current): ").strip()
    cgpa = float(cgpa_str) if cgpa_str else None

    print(f"Current Credits: {profile['completed_credits']}")
    credits_str = input("Enter completed credits (leave empty to keep current): ").strip()
    credits = float(credits_str) if credits_str else None

    update_profile(
        name=name if name else None,
        student_id=student_id if student_id else None,
        cgpa=cgpa,
        credits=credits,
    )
    print("\nProfile updated successfully!")


def browse_courses_menu():
    print_header("UIU CSE COURSE CATALOG & PREREQUISITES")
    catalog = list_courses()
    print(f"{'Code':<12}{'Credits':<10}{'Title':<35}{'Prerequisites'}")
    print("-" * 75)
    for code, info in catalog.items():
        prereqs = ", ".join(info["prerequisites"]) if info["prerequisites"] else "None"
        print(f"{code:<12}{info['credits']:<10.1f}{info['title']:<35}{prereqs}")

    print("\nCheck Prerequisite Eligibility:")
    test_code = input("Enter course code to test (or press Enter to skip): ").strip()
    if test_code:
        completed = input("Enter completed courses (comma separated, e.g., CSE1111, CSE2213): ").split(",")
        completed = [c.strip() for c in completed if c.strip()]
        result = check_prerequisites(test_code, completed)
        if result["can_take"]:
            print(f"ELIGIBLE! All prerequisites satisfied for {normalize_code(test_code)}.")
        else:
            print(f"INELIGIBLE! Missing prerequisites: {', '.join(result['missing'])}")


def waiver_probation_menu():
    print_header("ACADEMIC STANDING & WAIVER CHECKER")
    profile = get_profile()
    cgpa = input_number("Enter CGPA to evaluate", minimum=0, default=profile["current_cgpa"])

    probation_info = check_probation_status(cgpa)
    waiver_info = check_waiver_eligibility(cgpa)

    print()
    print("-" * 60)
    print(f"Academic Standing : {probation_info['status']}")
    print(f"Remarks           : {probation_info['message']}")
    print("-" * 60)
    print(f"Tuition Waiver    : {waiver_info['percentage']}%")
    print(f"Waiver Details    : {waiver_info['remarks']}")
    print("-" * 60)


def calculate_gpa_menu():
    print_header("GPA CALCULATOR")
    courses = []
    count = int(input_number("How many courses?", minimum=1))
    for i in range(1, count + 1):
        print(f"\nCourse {i}")
        courses.append(input_course())

    gpa = calculate_gpa(courses)
    print()
    print("-" * 60)
    print(f"GPA: {gpa:.2f}")
    print("-" * 60)


def calculate_cgpa_menu():
    print_header("CGPA CALCULATOR")
    courses = []
    count = int(input_number("How many courses/records?", minimum=1))
    for i in range(1, count + 1):
        print(f"\nCourse {i}")
        courses.append(input_course())

    cgpa = calculate_cgpa(courses)
    print()
    print("-" * 60)
    print(f"CGPA: {cgpa:.2f}")
    print("-" * 60)


def target_cgpa_menu():
    print_header("TARGET CGPA PLANNER")
    profile = get_profile()

    current_cgpa = input_number("Current CGPA", minimum=0, default=profile["current_cgpa"])
    completed_credits = input_number("Completed credits", minimum=0, default=profile["completed_credits"])
    future_credits = input_number("Future credits you will take", minimum=0.01)
    target_cgpa = input_number("Target CGPA", minimum=0)

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
    print("-" * 60)
    if required_gpa <= 0:
        print("Target CGPA is already achievable.")
    else:
        print(f"Required future GPA: {required_gpa:.2f}")

    if reachable:
        print("Status: TARGET IS MATHEMATICALLY REACHABLE")
    else:
        print("Status: TARGET IS NOT REACHABLE")
        print("You would need a future GPA above 4.00.")
    print("-" * 60)


def what_if_simulator_menu():
    print_header("WHAT-IF SIMULATOR")
    profile = get_profile()

    current_cgpa = input_number("Current CGPA", minimum=0, default=profile["current_cgpa"])
    current_credits = input_number("Current completed credits", minimum=0, default=profile["completed_credits"])
    count = int(input_number("How many future courses?", minimum=1))

    courses = []
    for i in range(1, count + 1):
        print(f"\nFuture Course {i}")
        courses.append(input_course())

    future_gpa = calculate_gpa(courses)
    future_credits = sum(course.credits for course in courses)
    total_credits = current_credits + future_credits

    new_cgpa = 0.0 if total_credits <= 0 else ((current_cgpa * current_credits) + (future_gpa * future_credits)) / total_credits
    target_cgpa = input_number("\nTarget CGPA (enter 0 to skip check)", minimum=0)

    print()
    print("-" * 60)
    print("Scenario")
    print("-" * 60)
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
    print("-" * 60)


def retake_impact_menu():
    print_header("RETAKE IMPACT CALCULATOR")
    profile = get_profile()

    current_cgpa = input_number("Current CGPA", minimum=0, default=profile["current_cgpa"])
    current_credits = input_number("Current total credits", minimum=0.01, default=profile["completed_credits"])
    count = int(input_number("How many courses are you retaking?", minimum=1))

    retakes = []
    for i in range(1, count + 1):
        print(f"\nRetake {i}")
        retakes.append(input_retake())

    old_total_points = current_cgpa * current_credits
    old_points_removed = sum(get_grade_point(r["old_grade"]) * r["credits"] for r in retakes)
    new_points_added = sum(get_grade_point(r["new_grade"]) * r["credits"] for r in retakes)

    new_total_points = old_total_points - old_points_removed + new_points_added
    new_cgpa = new_total_points / current_credits
    change = new_cgpa - current_cgpa

    print()
    print("-" * 60)
    print("Retake Summary")
    print("-" * 60)
    for r in retakes:
        print(f"{r['course_code']} ({r['credits']:.2f} cr): {r['old_grade']} -> {r['new_grade']}")

    print()
    print(f"{'Old CGPA':<18}: {current_cgpa:.2f}")
    print(f"{'New CGPA':<18}: {new_cgpa:.2f}")

    if change > 0:
        print(f"{'Change':<18}: +{change:.2f} (improved)")
    elif change < 0:
        print(f"{'Change':<18}: {change:.2f} (dropped)")
    else:
        print(f"{'Change':<18}: 0.00 (no change)")
    print("-" * 60)


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
        profile = get_profile()
        print_header(f"UIU STUDENT ASSISTANT — Welcome, {profile['name']}!")

        print("1. Calculate GPA")
        print("2. Calculate CGPA")
        print("3. Target CGPA Planner")
        print("4. View Grade Scale")
        print("5. What-if Simulator")
        print("6. Retake Impact Calculator")
        print("7. Browse Courses & Prerequisites")
        print("8. Academic Standing & Waiver Checker")
        print("9. Manage Profile")
        print("0. Exit")
        print()

        choice = input("Select an option: ").strip()
        try:
            if choice == "1": calculate_gpa_menu()
            elif choice == "2": calculate_cgpa_menu()
            elif choice == "3": target_cgpa_menu()
            elif choice == "4": show_grade_scale()
            elif choice == "5": what_if_simulator_menu()
            elif choice == "6": retake_impact_menu()
            elif choice == "7": browse_courses_menu()
            elif choice == "8": waiver_probation_menu()
            elif choice == "9": manage_profile_menu()
            elif choice == "0":
                print("\nThank you for using UIU Student Assistant.")
                break
            else:
                print("\nInvalid option. Please select 0-9.")
        except Exception as error:
            print(f"\nError: {error}")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
