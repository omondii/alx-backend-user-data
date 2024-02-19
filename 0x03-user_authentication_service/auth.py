#!/usr/bin/env python3
""" Password Hashing """
import bcrypt


def _hash_password(password: str) -> bytes:
    """ Hashes the given password """
    if password:
        salt = bcrypt.gensalt()
        pwd = password.encode('utf-8')
        hashed = bcrypt.hashpw(pwd, salt)
        return hashed
    else:
        return None