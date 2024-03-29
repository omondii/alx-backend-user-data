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

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Returns a user based on passed session_id """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """ Updates the corresponding session_id """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
            return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ If user is found, update the reset token """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                uuid = _generate_uuid()
                self._db.update_user(user.id, reset_token=uuid)
                return uuid
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ Updates password for corresponding reset_token """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed, reset_token=None)
