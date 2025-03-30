import random

class Database:
    def __init__(self):
        self.students = []
        self.lectures = []

    def addStudent(self, name, course, year):
        """Adds a student with additional details."""
        student = {
            "name": name,
            "course": course,
            "year": year,
            "attendance_percentage": round(random.uniform(50, 100), 2),
            "last_attended": random.choice([
                "Lecture 1", "Lecture 2", "Lecture 3", "Lecture 4"
            ]),
            "attended": False  # Default not attended for current session
        }
        self.students.append(student)

    def addLecture(self, lecture_name, lecturer, students):
        """Adds a lecture with the lecturer and enrolled students."""
        lecture = {
            "name": lecture_name,
            "lecturer": lecturer,
            "students": students
        }
        self.lectures.append(lecture)

    def getStudents(self):
        return self.students

    def getLectures(self):
        return self.lectures

# Example Data
courses = ["Mechatronics", "Electronic Engineering", "Electrical Engineering"]
years = [1, 2, 3, 4, 5]

# Instantiate Database
db = Database()

db.addStudent("Tyler", random.choice(courses), random.choice(years))
db.addStudent("Conor", random.choice(courses), random.choice(years))
db.addStudent("Jamie", random.choice(courses), random.choice(years))
db.addStudent("Harrison", random.choice(courses), random.choice(years))

# Add Lectures
db.addLecture("Advanced Robotics", "Dr. Smith", ["Tyler", "Conor"])
db.addLecture("Embedded Systems", "Prof. Johnson", ["Jamie", "Harrison"])
db.addLecture("AI in Engineering", "Dr. Brown", ["Tyler", "Harrison"])
db.addLecture("Signal Processing", "Dr. Williams", ["Conor", "Jamie"])

# Print Data
print("Students:")
for student in db.getStudents():
    print(student)

print("\nLectures:")
for lecture in db.getLectures():
    print(lecture)
