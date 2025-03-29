import serial
import apiRequests


# Open serial connection (Check your port with `ls /dev/tty*`)
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

while True:
    line = ser.readline().decode('utf-8').strip()
    if line:
        print("Received:", line)

        # Check if the input follows the format "StudentName: tyler"
        if line.startswith("StudentName:"):
            student_name = line.split(":")[1].strip()  # Extract the name
            apiRequests.attend_student(student_name)  # Call the function with the extracted name
