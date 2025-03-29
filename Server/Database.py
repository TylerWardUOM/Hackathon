class Database:
    def __init__(self):
        self.students = []  # List of dictionaries for easier updates

    def attendStudent(self, StudentName):
        """Adds a student with a default False (not verified) flag."""
        if not any(student["name"] == StudentName for student in self.students):  
            self.students.append({"name": StudentName, "attended": False})

    def verifyStudent(self, StudentName):
        """Updates the student's attendance flag to True if they exist in the list."""
        for student in self.students:
            if student["name"] == StudentName:
                student["attended"] = True
                return True  # Return True if student found and updated
        return False  # Return False if student not found

    def getStudents(self):
        """Returns the list of students with their verification status."""
        return self.students


# Example usage:
db = Database()
db.attendStudent("Alice")
db.attendStudent("Bob")

print(db.getStudents())  # [{'name': 'Alice', 'attended': False}, {'name': 'Bob', 'attended': False}]

db.verifyStudent("Alice")
print(db.getStudents())  # [{'name': 'Alice', 'attended': True}, {'name': 'Bob', 'attended': False}]
