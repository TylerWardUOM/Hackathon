import sqlite3

class Database:
    def __init__(self):
        self.attended_students = []  # List of dictionaries of Currently Attended Students
        self.db_name = 'university.db'
        self.studentBuffer = []

    def attendStudent(self, StudentName):
        """Adds a student with a default False (not verified) flag."""
        if not any(student["name"] == StudentName for student in self.attended_students):  
            self.attended_students.append({"name": StudentName, "verified": False})
            self.studentBuffer.append(StudentName)

    def verifyStudent(self, StudentName):
        """Updates the student's verified flag to True if they exist in the list."""
        for student in self.attended_students:
            if student["name"] == StudentName:
                student["verified"] = True
                return True  # Return True if student found and updated
        return False  # Return False if student not found

    def getStudents(self, lecture_name):
        """Returns the list of students registered for a specific lecture, 
        including their attendance status (verified or not)."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Query to join student, lecture_registration, and lecture tables
        cursor.execute('''
        SELECT s.name, s.course, s.year, s.attendance_percentage
        FROM student s
        JOIN lecture_registration lr ON s.id = lr.student_id
        JOIN lecture l ON lr.lecture_id = l.id
        WHERE l.lecture_name = ?
        ''', (lecture_name,))

        students = cursor.fetchall()
        conn.close()

        # Combine the data from the database with the current students' verified status
        student_list = []
        for student in students:
            # Find the corresponding student from self.students
            found_student = None
            for student_local in self.attended_students:
                if student_local["name"] == student[0]:
                    found_student = student_local
                    break  # Once found, break the loop

            if found_student:
                # Keep the attendance as it is, don't mark as verified automatically
                student_list.append({
                    "name": student[0], 
                    "course": student[1], 
                    "year": student[2], 
                    "attendance_percentage": student[3],
                    "attendance_status": True,
                    "Verified": True if found_student['verified'] else False,

                })
            else:
                # If student not found in the current list, treat as absent
                student_list.append({
                    "name": student[0], 
                    "course": student[1], 
                    "year": student[2], 
                    "attendance_percentage": student[3],
                    "attendance_status": False,
                    "Verified": False,
                })

        return student_list

    def getNext(self):
        if len(self.studentBuffer)!=0:
            next=self.studentBuffer[0]
            self.studentBuffer.pop(0)
        else:
            next=None
        return next

# # Example usage:
# db = Database()

# # Add some students to the list
# db.attendStudent("Jamie")
# db.attendStudent("Harrison")
# db.attendStudent("Tyler")

# # Verify Alice's attendance (doesn't affect the attendance status directly)
# db.verifyStudent("Tyler")

# # Fetch students for a specific lecture
# students_in_lecture = db.getStudents("Advanced Robotics")
# print(students_in_lecture)

# print(db.getNext())
# print(db.getNext())
# print(db.getNext())
# print(db.getNext())
# print(db.getNext())