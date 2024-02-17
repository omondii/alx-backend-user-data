#!/usr/bin/env python3
""" Module to handle all session authentication routes """
from api.v1.views import app_views
from flask import request, jsonify
from models.user import User
from flask import make_response
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ Handles user login and session creation
    """
    mail = request.form.get('email')
    if not mail:
        return jsonify({"error": "email missing"}), 400
    pwd = request.form.get('password')
    if not pwd:
        return jsonify({"error": "password missing"}), 400
    
    user = User.search({"email": mail})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    else:
        if not user.is_valid_password(pwd):
            return jsonify({"error": "wrong password"}), 401

        from api.v1.app import auth
        sess_Id = auth.create_session(user.id)
        user_dict = user.to_json()

        response = make_response(user_dict)
        sess_name = os.getenv('SESSION_NAME')
        response.set_cookie(sess_name, sess_Id)
        return response
