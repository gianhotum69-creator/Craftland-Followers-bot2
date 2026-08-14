from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "Vercel Python API is working"
    })

@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "success": True,
        "status": "online"
    })
