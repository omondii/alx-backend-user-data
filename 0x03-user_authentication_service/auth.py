#!/usr/bin/env python3
""" auth module  """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ takes in a password string arguments and returns bytes. """
    if password:
        salt = bcrypt.gensalt()
        pwd = password.encode('utf-8')
        hashed = bcrypt.hashpw(pwd, salt)
        return hashed
    else:
        return None


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers a user to the db """
        if email is None or password is None:
            raise ValueError("Email and password cannot be None")

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            try:
                hash_pwd = _hash_password(password)
                user = self._db.add_user(email=email, hashed_password=hash_pwd)
                return user
            except ValueError:
                raise ValueError("User <user's email> already exists")
        else:
            raise ValueError(f"User {email} already exists")
