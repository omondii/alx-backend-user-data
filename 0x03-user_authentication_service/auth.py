#!/usr/bin/env python3
""" Password Hashing """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ Hashes the given password """
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
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        
        if user is None:
            try:
                hashed_pwd = _hash_password(password)
                new_user = self._db.add_user(email, hashed_pwd)
                return new_user
            except ValueError:
                raise ValueError("User <user's email> already exists")
        else:
            raise ValueError(f"User {email} exists")