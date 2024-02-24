#!/usr/bin/env python3
""" auth module  """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """ takes in a password string arguments and returns bytes. """
    if password:
        salt = bcrypt.gensalt()
        pwd = password.encode('utf-8')
        hashed = bcrypt.hashpw(pwd, salt)
        return hashed
    else:
        return None


def _generate_uuid() -> str:
    """ Returns a string rep of a new UUID """
    id = uuid.uuid4()
    return str(id)


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

    def valid_login(self, email: str, password: str) -> bool:
        """ Checks for valid password """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                password = password.encode('utf-8')
                user_pwd = user.hashed_password
                if bcrypt.checkpw(password, user_pwd):
                    return True
                else:
                    return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ Creates a session Id for a user """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id
        except NoResultFound:
            return None
