from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/notifications', methods=['POST'])
def notifications():
    data = request.json
    print(f"Notification received: {data}")
    return jsonify({"status": "success", "message": "Notification received"}), 200

if __name__ == '__main__':
    app.run(port=5001)
