import sqlite3

# Function to create the SQLite database
def create_database():
    # Connect to SQLite database (it will create the database if it doesn't exist)
    conn = sqlite3.connect('university.db')
    cursor = conn.cursor()

    # Create the 'student' table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS student (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        course TEXT NOT NULL,
        year INTEGER NOT NULL,
        attendance_percentage REAL NOT NULL
    )
    ''')

    # Create the 'lecture' table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lecture (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lecture_name TEXT NOT NULL,
        lecturer_name TEXT NOT NULL,
        student_count INTEGER NOT NULL
    )
    ''')

    # Create the 'lecture_registration' table to link students to lectures
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lecture_registration (
        lecture_id INTEGER,
        student_id INTEGER,
        FOREIGN KEY(lecture_id) REFERENCES lecture(id),
        FOREIGN KEY(student_id) REFERENCES student(id),
        PRIMARY KEY (lecture_id, student_id)
    )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Function to add a student to the database
def add_student(name, course, year, attendance_percentage):
    conn = sqlite3.connect('university.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO student (name, course, year, attendance_percentage)
    VALUES (?, ?, ?, ?)
    ''', (name, course, year, attendance_percentage))

    conn.commit()
    conn.close()

# Function to add a lecture to the database
def add_lecture(lecture_name, lecturer_name, student_count):
    conn = sqlite3.connect('university.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO lecture (lecture_name, lecturer_name, student_count)
    VALUES (?, ?, ?)
    ''', (lecture_name, lecturer_name, student_count))

    conn.commit()
    conn.close()

# Function to register a student for a lecture
def register_student_for_lecture(lecture_id, student_id):
    conn = sqlite3.connect('university.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO lecture_registration (lecture_id, student_id)
    VALUES (?, ?)
    ''', (lecture_id, student_id))

    conn.commit()
    conn.close()

# Example usage
if __name__ == "__main__":
    create_database()

    # Add some students
    add_student("Tyler", "Mechatronics", 2, 88.5)
    add_student("Conor", "Electronic Engineering", 1, 92.0)
    add_student("Jamie", "Electrical Engineering", 3, 76.5)
    add_student("Harrison", "Mechatronics", 4, 85.0)

    # Add some lectures
    add_lecture("Advanced Robotics", "Dr. Smith", 3)
    add_lecture("Embedded Systems", "Prof. Johnson", 3)
    add_lecture("AI in Engineering", "Dr. Brown", 2)
    add_lecture("Signal Processing", "Dr. Williams", 4)

    # Register students for lectures (example)
    register_student_for_lecture(1, 1)  # Tyler in Advanced Robotics
    register_student_for_lecture(1, 2)  # Conor in Advanced Robotics
    register_student_for_lecture(1, 3)  # Jamie 
    register_student_for_lecture(1, 4)  # Harrison 

    print("Data added successfully!")
