
grades = { "Alice": 85,"Bob": 92,"Charlie": 78,"David": 90, 
    "Emma": 88}

def display_gradebook():
    if not grades:
        print("Gradebook is empty")
    else:
        print("\nStudent Gradebook:")
        for student, grade in grades.items():
            print(f"{student} -> {grade}")

def search_student():
    name = input("Enter student name to search: ")
    if name in grades:
        print(f"{name}’s grade is: {grades[name]}")
    else:
        print("Student not found")

def update_grade():
    name = input("Enter student name to update: ")
    if name in grades:
        try:
            new_grade = int(input(f"Enter new grade for {name}: "))
            old_grade = grades[name]
            grades[name] = new_grade
            print(f"Updating grade: {name} -> {old_grade} to {new_grade}")
        except ValueError:
            print("Invalid grade... Please enter a number.")
    else:
        print("Student not found")

def find_top_student():
    if not grades:
        print("Gradebook is empty")
        return
    top_name = None
    top_grade = -1
    for name, grade in grades.items():
        if grade > top_grade:
            top_name = name
            top_grade = grade
    print(f"Top student: {top_name} with grade {top_grade}")

def main_menu():
    while True:
        print("\n==== STUDENT GRADEBOOK MENU ====")
        print("1. Display All Grades")
        print("2. Search Student")
        print("3. Update Grade")
        print("4. Find Top Student")
        print("5. Exit")

        choice = input("Choose an option (1-5): ")

        if choice == "1":
            display_gradebook()
        elif choice == "2":
            search_student()
        elif choice == "3":
            update_grade()
        elif choice == "4":
            find_top_student()
        elif choice == "5":
            print("Goodbye!!!")
            break
        else:
            print("Invalid choice... Please enter a number from 1 to 5.")

main_menu()
