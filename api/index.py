from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "Craftland Followers Bot API"
    })

@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "success": True,
        "status": "online"
    })

@app.route("/send", methods=["POST"])
def send():
    data = request.get_json(silent=True) or {}

    uid = data.get("uid")
    region = data.get("region")

    if not uid:
        return jsonify({
            "success": False,
            "message": "uid is required"
        }), 400

    return jsonify({
        "success": True,
        "message": "Request received",
        "uid": str(uid),
        "region": region
    })

if __name__ == "__main__":
    app.run()
