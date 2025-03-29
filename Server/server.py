from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "Running", "device": "Raspberry Pi"})

# Example: Receive data via POST request
@app.route('/attend', methods=['POST'])
def receive_data():
    data = request.json  # Get Student Name from request
    
    if not data or "studentName" not in data:
        return jsonify({"error": "Missing 'studentName' in request"}), 400

    return jsonify({"Marked as Attended": data["studentName"]})

# Run the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Allow connections from any device
