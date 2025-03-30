from flask import Flask, jsonify, request
from Database import Database

database=Database()

app = Flask(__name__)


@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "Running", "device": "Raspberry Pi"})

# Example: Receive data via POST request
@app.route('/attend', methods=['POST'])
def attend():
    data = request.json  # Get Student Name from request
    
    if not data or "studentName" not in data:
        return jsonify({"error": "Missing 'studentName' in request"}), 400

    database.attendStudent(data["studentName"])
    return jsonify({"Marked as Attended": data["studentName"]})

@app.route('/attendance', methods=['POST'])
def attendance():
    data = request.json  # Get Student Name from request
    if not data or "lectureName" not in data:
        return jsonify({"error": "Missing 'lectureName' in request"}), 400
    return jsonify({"attended": database.getStudents(data["lectureName"])})


@app.route('/verify', methods=['POST'])
def verify():
    data = request.json  # Get Student Name from request
    
    if not data or "studentName" not in data:
        return jsonify({"error": "Missing 'studentName' in request"}), 400

    database.verifyStudent(data["studentName"])
    return jsonify({"Marked as Verified": data["studentName"]})
# Run the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Allow connections from any device
