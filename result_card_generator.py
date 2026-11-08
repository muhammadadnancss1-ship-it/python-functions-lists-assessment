'''Topic: Functions (def, parameters, return) and strings

Build a Python program that creates a result card for one student.

Your program must:

Ask for student name, roll number and marks in 5 subjects.
Write at least these functions: get_valid_marks(subject), 
calculate_percentage(total, max_total), get_grade(percentage), format_name(name).
Validate input: marks 0-100, roll number made of digits only (.isdigit()).
Clean the name with string methods: .strip() and .title().
Grades: 90+ A+, 80-89 A, 70-79 B, 60-69 C, 50-59 D, below 50 Fail.
If any subject is below 40, the result is Fail, whatever the percentage.
Print a neat result card using f-strings (name, roll number, each subject, 
total, percentage with 2 decimals, grade, Pass/Fail).'''


print("==================Result Card Generator================")


# Remove extra spaces and capitalize the student's name
def format_name(name):
    return name.strip().title()


# Take marks and make sure they are valid
def get_valid_marks(subject):
    while True:
        marks = input(f"Enter marks for {subject}: ").strip()

        # First check if the input contains only numbers
        if not marks.isdigit():
            print("Invalid marks! Please enter numbers only.")

        # Check if the marks are between 0 and 100
        elif int(marks) > 100:
            print("Invalid marks! Enter marks between 0 and 100.")

        else:
            return int(marks)


# Calculate the student's percentage
def calculate_percentage(total, max_total):
    return (total / max_total) * 100


# Give a grade according to the percentage
def get_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "Fail"


# Get the student's name and check if it contains only letters
while True:
    name = input("Enter student name: ").strip()

    if name.replace(" ", "").isalpha():
        name = format_name(name)
        break
    else:
        print("Invalid name! Please enter letters only.")


# Get the roll number and check if it contains only digits
while True:
    roll_number = input("Enter roll number: ").strip()

    if roll_number.isdigit():
        break
    else:
        print("Invalid roll number! Please enter digits only.")


# Store the subjects and their marks
subjects = ["English", "Math", "Physics", "Chemistry", "Computer"]
marks = []

# Take marks for all five subjects
for subject in subjects:
    marks.append(get_valid_marks(subject))


# Calculate total marks, percentage and grade
total = sum(marks)
percentage = calculate_percentage(total, 500)
grade = get_grade(percentage)


# If any subject has less than 40 marks, the student fails
if min(marks) < 40:
    grade = "Fail"


# Check the final pass or fail result
if grade == "Fail":
    result = "Fail"
else:
    result = "Pass"


# Print the complete student result card
print("\n========== STUDENT RESULT CARD ==========")
print(f"Student Name : {name}")
print(f"Roll Number  : {roll_number}")
print("-----------------------------------------")

# Show marks for each subject
for i in range(5):
    print(f"{subjects[i]:12}: {marks[i]}/100")

# Show the total marks, percentage, grade and result
print("-----------------------------------------")
print(f"Total Marks  : {total}/500")
print(f"Percentage   : {percentage:.2f}%")
print(f"Grade        : {grade}")
print(f"Result       : {result}")
print("=========================================")

