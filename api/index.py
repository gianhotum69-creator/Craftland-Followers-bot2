from flask import Flask, jsonify

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

if __name__ == "__main__":
    app.run()
