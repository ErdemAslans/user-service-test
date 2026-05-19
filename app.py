import re
from flask import Flask, jsonify, request

app = Flask(__name__)

# Simple in-memory user store (resets on app restart). Not for production.
_USERS: list[dict] = []

# Basic email regex for validation
EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


@app.route("/users/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Add email format validation
    if not re.match(EMAIL_REGEX, email):
        return jsonify({"error": "Invalid email format"}), 400

    _USERS.append({"email": email, "password": password})
    return jsonify({"email": email, "id": len(_USERS)}), 201


@app.route("/users", methods=["GET"])
def list_users():
    return jsonify([{"email": u["email"], "id": idx + 1} for idx, u in enumerate(_USERS)])


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
