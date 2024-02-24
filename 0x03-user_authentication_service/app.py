#!/usr/bin/env python3
""" Flask module """
from flask import Flask, jsonify, request
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    """Returns a json payload"""
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=['POST'])
def users():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        Auth.register_user(email, password)
        return jsonify({"email": "<registered email>", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000',
            debug=True)