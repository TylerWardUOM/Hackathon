class Database():
    def __init__(self):
        self.students = []  # List of tuples (StudentName, AttendedFlag)

    def attendStudent(self, StudentName):
        """Adds a student with a default False (not verified) flag."""
        self.students.append((StudentName, False))

    def verifyStudent(self, StudentName):
        """Updates the student's attendance flag to True if they exist in the list."""
        for i in range(len(self.students)):
            name = self.students[i][0]
            if name == StudentName:
                self.students[i] = (name, True)  # Update flag to True
                return True  # Return True if student found and updated
        return False  # Return False if student not found

    def getStudents(self):
        """Returns the list of students with their verification status."""
        return self.students


# Example usage:
db = Database()
db.attendStudent("Alice")
db.attendStudent("Bob")

print(db.getStudents())  # [('Alice', False), ('Bob', False)]

db.verifyStudent("Alice")
print(db.getStudents())  # [('Alice', True), ('Bob', False)]
