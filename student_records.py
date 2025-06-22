import sqlite3

# connect to / create the database
conn = sqlite3.connect("student_records.db")
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

##############################################
# Table Setup Function
##############################################
def create_tables():
    # "students" table containing student names and auto-incrementing as added student ID's
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL UNIQUE
        );
    """)

    # "competencies" table containing compentency titles and auto-incrementing as added competency ID's
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competencies (
            competency_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            title TEXT NOT NULL UNIQUE
        );
    """)

    # "grades" table containing grades and auto-incrementing as added grade ID's. Each grade is linked to a student and competency
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            competency_id INTEGER,
            grade INTEGER CHECK (grade BETWEEN 1 AND 4),
            FOREIGN KEY(student_id) REFERENCES students(student_id),
            FOREIGN KEY(competency_id) REFERENCES competencies(competency_id)
        );
    """)

    conn.commit()



##############################################
# Functions to add to or update tables
##############################################
"""
Adds parameter "name" to the students table. 
Automatically given the next student_id number.
"""
def add_student(name):
    cursor.execute("INSERT INTO students (name) VALUES (?)", (name,))
    conn.commit()
    print(f"\nStudent '{name}' added.")



"""
Adds parameter "title" to the competencies table. 
Automatically given the next competency_id number.
"""
def add_competency(title):
    cursor.execute("INSERT INTO competencies (title) VALUES (?)", (title,))
    conn.commit()
    print(f"\nCompetency '{title}' added.")



"""
Assigns a competency level for a certain competency and certain student.
Can pass in as parameters either the student/competency name/title or their ID's.
At least one for the student and one for the competency is required.
"""
def assign_grade(level_number, student_id, student_name, competency_id, competency_title):
    # updates table with new competency level
    cursor.execute("""
        INSERT OR REPLACE INTO grades (student_id, competency_id, grade)
        VALUES (?, ?, ?)
    """, (student_id, competency_id, level_number))
    conn.commit()

    print(f"\nRecorded '{get_level_name_from_number(level_number)}' ({level_number}) for student {student_name} ({student_id}) on competency {competency_id}, {competency_title}.")



##################################################################
# Functions to delete from tables
##################################################################
def delete_student(student_id, student_name):
    cursor.execute("DELETE FROM grades WHERE student_id = ?", (student_id,))
    cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()
    print(f"\nStudent {student_name} ({student_id}) and their associated grades were deleted.")

def delete_competency(competency_id, competency_name):
    cursor.execute("DELETE FROM grades WHERE competency_id = ?", (competency_id,))
    cursor.execute("DELETE FROM competencies WHERE competency_id = ?", (competency_id,))
    conn.commit()
    print(f"\nCompetency {competency_id}, {competency_name}, and its associated grades were deleted.")



##################################################################
# Functions for getting names, competency titles or eithers ID's
##################################################################
"""
The following four functions gets the names/titles from an ID or 
gets the ID from a name/title for students and competencies
"""
def get_student_id_by_name(name):
    cursor.execute("SELECT student_id FROM students WHERE name = ?", (name,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_student_name_by_id(student_id):
    cursor.execute("SELECT name FROM students WHERE student_id = ?", (student_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_competency_id_by_title(title):
    cursor.execute("SELECT competency_id FROM competencies WHERE title = ?", (title,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_competency_title_by_id(competency_id):
    cursor.execute("SELECT title FROM competencies WHERE competency_id = ?", (competency_id,))
    result = cursor.fetchone()
    return result[0] if result else None

"""
This function gets the student id and name from whichever other one is provided.
Returns tuple (None, None) if student doesnt exist or neither name or ID provided. 
Returns tuple (student_id, student_name) if valid and one is provided
"""
def resolve_student(input_value):
    try:
        # Try converting to int: if successful, assume it's an ID
        student_id = int(input_value)
        student_name = get_student_name_by_id(student_id)
        if student_name is None:
            print(f"No student found with ID '{student_id}'.")
            return None, None
        return student_id, student_name
    except ValueError:
        # If not an integer, treat it as a name
        student_name = input_value
        student_id = get_student_id_by_name(student_name)
        if student_id is None:
            print(f"No student found with name '{student_name}'.")
            return None, None
        return student_id, student_name


"""
This function gets the competency id and title from whichever other one is provided.
Returns tuple (None, None) if competency doesnt exist or neither title or ID provided.
Returns tuple (competency_id, competency_title) if valid and one is provided
"""
def resolve_competency(input_value):
    try:
        competency_id = int(input_value)
        competency_title = get_competency_title_by_id(competency_id)
        if competency_title is None:
            print(f"No competency found with ID '{competency_id}'.")
            return None, None
        return competency_id, competency_title
    except ValueError:
        competency_title = input_value
        competency_id = get_competency_id_by_title(competency_title)
        if competency_id is None:
            print(f"No competency found with title '{competency_title}'.")
            return None, None
        return competency_id, competency_title



"""
Gets the name of one of the four competency levels based on level number parameter
"""
def get_level_name_from_number(level):
    return {
        1: "Beginning",
        2: "Developing",
        3: "Proficient",
        4: "Advanced"
    }.get(level, "Unknown")



##############################################
# Function to generate competency report
##############################################
"""
Generates the full competency report for a student
"""
def generate_student_report(student_id, student_name):
    print(f"\nReport for student {student_name} ({student_id}):")

    # gets the student's information for the report
    cursor.execute("""
        SELECT c.competency_id, c.title, g.grade
        FROM grades g
        JOIN students s ON g.student_id = s.student_id
        JOIN competencies c ON g.competency_id = c.competency_id
        WHERE s.student_id = ?
    """, (student_id,))
    records = cursor.fetchall()

    # displays each competency and coresponding level for the student
    for row in records:
        competency_id = row[0]
        competency_title = row[1]
        level_number = row[2]
        level_name = get_level_name_from_number(level_number)
        print(f"\tCompetency {competency_id}, {competency_title}   |   {level_name} ({level_number})")

    print("\n\t----------------------------------------------------------------------------\n")
    # counts the amount of each level for the student
    cursor.execute("""
        SELECT grade, COUNT(*) FROM grades
        WHERE student_id = ?
        GROUP BY grade
        ORDER BY grade DESC
        """, (student_id,))
    
    # displays amount of each level for the student
    print("\tCompetency Amount Summary:")
    for level_number, count in cursor.fetchall():
        print(f"\t\t{get_level_name_from_number(level_number)} ({level_number}): {count}")

    print("\n")

    
##############################################
# Main function with menu for actions
##############################################
def main():
    while True:
        # menu list 
        print("\n--- Student Record Manager ---")
        print("1. Add Student")
        print("2. Add Competency")
        print("3. Assign Grade")
        print("4. Generate Student Report")
        print("5. Delete Student")
        print("6. Delete Competency")
        print("7. Exit")
        choice = input("Select an option: ")


        # Add Student
        if choice == '1':
            name = input("Student name: ")
            add_student(name)


        # Add Competency
        elif choice == '2':
            title = input("Competency title: ")
            add_competency(title)


        # Assign Grade
        elif choice == '3':
            # get the student name and id
            student_input = input("Student name or ID: ")
            student_id, student_name = resolve_student(student_input)
            if (student_id, student_name) != (None, None): # if student does not exist, restart the menu
                # get the competency title and id
                competency_input = input("Competency title or ID: ")
                competency_id, competency_title = resolve_competency(competency_input)
                if (competency_id, competency_title) != (None, None): # if competency does not exist, restart the menu
                    # get the competency level
                    print("Enter competency level (1 = Beginning, 2 = Developing, 3 = Proficient, 4 = Advanced)")
                    try:
                        level = int(input("Level: "))
                        if level not in [1, 2, 3, 4]:
                            raise ValueError
                    except ValueError:
                        print("Invalid level. Must be an integer from 1 to 4.")
                        continue # if invalid level, restart the menu

                    assign_grade(level, student_id, student_name, competency_id, competency_title)


        # Generate Student Report
        elif choice == '4':
            # get student name and id
            student_input = input("Student name or ID: ")
            student_id, student_name = resolve_student(student_input)
            if (student_id, student_name) != (None, None): # if student does not exist, restart the menu
                generate_student_report(student_id, student_name)


        # Delete Student
        elif choice == '5':
            student_input = input("Student name or ID to delete: ")
            student_id, student_name = resolve_student(student_input)
            if (student_id, student_name) != (None, None): # if student does not exist, restart the menu
                delete_student(student_id, student_name) 


        # Delete Competency
        elif choice == '6':
            competency_input = input("Competency title or ID to delete: ")
            competency_id, competency_title = resolve_competency(competency_input)
            if (competency_id, competency_title) != (None, None): # if competency does not exist, restart the menu
                delete_competency(competency_id, competency_title)

        # Exit
        elif choice == '7':
            print("Exiting student record manager...")
            break


        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    create_tables()
    main()
    conn.close()