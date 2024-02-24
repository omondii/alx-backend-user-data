#!/usr/bin/env python3
""" Flask module """
from flask import Flask, jsonify, request, abort, redirect
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
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'])
def login() -> str:
    """ Validates login info provided """
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email=email)
        response = jsonify({"email": "<user email>", "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    abort(401)


@app.route("/sessions", methods=['DELETE'])
def logout() -> str:
    """ Deletes session for given id """
    try:
        session_id = request.cookies.get('session_id')
        if session_id:
            user = AUTH.get_user_from_session_id(session_id)
            if user:
                AUTH.destroy_session(user.id)
                return redirect('/')
        else:
            abort(403)
    except ValueError:
        abort(403)


@app.route("/profile", methods=['GET'])
def profile():
    """ Uses session id to retrieve user profile """
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email}), 200
        abort(403)
    abort(403)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """ Returns a reset token """
    email = request.form.get('email')
    if email:
        try:
            token = AUTH.get_reset_password_token(email)
        except ValueError:
            abort(403)
        return jsonify({"email": email, "reset_token": token}), 200


@app.route("/reset_password", methods=['PUT'])
def update_password():
    """ Updates user password based on reset_token """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000',
            debug=True)
