import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# Simple in-memory user store (resets on app restart). Not for production.
_USERS: list[dict] = []

APP_VERSION = "1.0.0"


@app.route("/users/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # NOTE: email format validation is intentionally missing.
    # AI agent should add it to satisfy TASK-123.

    _USERS.append({"email": email, "password": password})
    return jsonify({"email": email, "id": len(_USERS)}), 201


@app.route("/users", methods=["GET"])
def list_users():
    return jsonify([{"email": u["email"], "id": idx + 1} for idx, u in enumerate(_USERS)])


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/version", methods=["GET"])
def version():
    return jsonify({"version": APP_VERSION}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
