from flask import Flask, jsonify, request
from Database import Database
from flask_cors import CORS  # Import CORS

database=Database()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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

@app.route('/attendance', methods=['GET'])
def attendance():
    return jsonify({"attended": database.getStudents()})


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
