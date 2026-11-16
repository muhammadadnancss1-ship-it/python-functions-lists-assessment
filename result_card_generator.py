"""Create one student's result card using functions, strings and a marks list."""

SUBJECTS = ["English", "Math", "Physics", "Chemistry", "Computer"]
MIN_MARKS = 0
MAX_MARKS = 100
MAX_TOTAL = len(SUBJECTS) * MAX_MARKS
SUBJECT_PASS_MARK = 40
GRADE_A_PLUS = 90
GRADE_A = 80
GRADE_B = 70
GRADE_C = 60
GRADE_D = 50
MAX_INTEGER_DIGITS = 18


def format_name(name):
    """Remove surrounding whitespace and apply Python's title casing."""
    return name.strip().title()


def get_valid_marks(subject):
    """Read a whole-number mark from 0 to 100; retry invalid input."""
    while True:
        text = input(f"Enter marks for {subject}: ").strip()
        # isdecimal() excludes digit symbols such as ² that int() cannot read.
        if not text.isdecimal():
            print("Invalid marks! Please enter numbers only.")
            continue

        normalized = text.lstrip("0") or "0"
        # Bound conversion before int(); long invalid input must not crash.
        if len(normalized) > MAX_INTEGER_DIGITS:
            print(f"Invalid marks! Enter marks between {MIN_MARKS} and {MAX_MARKS}.")
            continue

        value = int(normalized)
        if MIN_MARKS <= value <= MAX_MARKS:
            return value
        print(f"Invalid marks! Enter marks between {MIN_MARKS} and {MAX_MARKS}.")


def calculate_percentage(total, max_total):
    """Calculate a percentage; the application always supplies MAX_TOTAL."""
    return (total / max_total) * 100


def get_grade(percentage):
    """Return the percentage grade; main() applies the subject-fail override."""
    if percentage >= GRADE_A_PLUS:
        return "A+"
    elif percentage >= GRADE_A:
        return "A"
    elif percentage >= GRADE_B:
        return "B"
    elif percentage >= GRADE_C:
        return "C"
    elif percentage >= GRADE_D:
        return "D"
    return "Fail"


def main():
    """Collect validated details, calculate the result and print the card."""
    print("==================Result Card Generator================")

    while True:
        name = input("Enter student name: ").strip()
        if name.replace(" ", "").isalpha():
            name = format_name(name)
            break
        print("Invalid name! Please enter letters only.")

    while True:
        roll_number = input("Enter roll number: ").strip()
        # Keep IDs as text so leading zeros are preserved.
        if roll_number.isdigit():
            break
        print("Invalid roll number! Please enter digits only.")

    marks = []
    for subject in SUBJECTS:
        marks.append(get_valid_marks(subject))

    total = sum(marks)
    percentage = calculate_percentage(total, MAX_TOTAL)
    grade = get_grade(percentage)
    if min(marks) < SUBJECT_PASS_MARK:
        grade = "Fail"
    result = "Fail" if grade == "Fail" else "Pass"

    print("\n========== STUDENT RESULT CARD ==========")
    print(f"Student Name : {name}")
    print(f"Roll Number  : {roll_number}")
    print("-----------------------------------------")
    for index in range(len(SUBJECTS)):
        print(f"{SUBJECTS[index]:12}: {marks[index]}/{MAX_MARKS}")
    print("-----------------------------------------")
    print(f"Total Marks  : {total}/{MAX_TOTAL}")
    print(f"Percentage   : {percentage:.2f}%")
    print(f"Grade        : {grade}")
    print(f"Result       : {result}")
    print("=========================================")


if __name__ == "__main__":
    main()
