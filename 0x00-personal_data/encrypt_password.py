#!/usr/bin/env python3
""" Password encryption module """
import bcrypt


def hash_password(password: str) -> str:
    """ Encrypts passwords using the bycrpt package """
    if password is None:
        return None
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed
