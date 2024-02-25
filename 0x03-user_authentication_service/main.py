#!/usr/bin/env python3
"""
Tests file
"""
import requests
from flask import jsonify
from user import User

URL = "http://localhost:5000/"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """ Test to validate user registration endpoint
        /users
    """
    data = {
        "email": EMAIL,
        "password": PASSWD
    }
    response = requests.post(f"{URL}/users", data=data)
    msg = {"email": email, "message": "user created"}

    assert response.status_code == 200
    assert response.json() == msg


def log_in_wrong_password(email: str, password: str) -> None:
    """ Validates response to a wrong password login
        /sessions
    """
    data = {
        "email": EMAIL,
        "password": NEW_PASSWD
    }

    response = requests.post(f"{URL}/sessions", data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> None:
    """ Validates login with correct details endpoint
        /sessions
    """
    data = {
        "email": EMAIL,
        "password": PASSWD
    }
    response = requests.post(f"{URL}/sessions", data=data)

    msg = {"email": email, "message": "logged in"}
    assert response.status_code == 200
    assert response.json() == msg


def profile_unlogged() -> None:
    """ Gets User profile before user login endpoint
        /profile
    """
    data = {
        "session_id": ""
    }

    response = requests.get(f"{URL}/profile", data=data)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """ Gets profile of a logged in user endpoint
        /profile
    """
    data = {
        "session_id": session_id
    }

    msg = {"email": EMAIL}
    response = requests.post(f"{URL}/profile", data=data)
    assert response.status_code == 200
    assert response.json() == msg


def log_out(session_id: str) -> None:
    """ Tests Logout endpoint
        /sessions
    """
    data = {
        "session_id": session_id
    }
    msg = {"message": "Bienvenue"}

    response = requests.delete(f"{URL}/sessions", data=data)
    assert response.status_code == 200
    assert response.json() == msg


def reset_password_token(email: str) -> str:
    """ Tests password reset token endpoint
        /sessions
    """
    data = {
        "email": EMAIL
    }
    token = response.json().get("reset_token")
    msg = {"email": email, "reset_token": token}
    response = requests.delete(f"{URL}/sessions", data=data)

    assert response.status_code == 200
    assert response.json() == msg


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Validates update password endpoint
        /reset_password
    """
    data = {
        "email": EMAIL,
        "reset_token": reset_token,
        "new_password": NEW_PASSWD
    }

    response = requests.put(f"{URL}/reset_password", data=data)
    msg = {"email": email, "message": "Password updated"}

    assert response.status_code == 200
    assert response.json() == msg


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
