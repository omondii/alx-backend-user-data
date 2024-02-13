#!/usr/bin/env python3
""" auth.py """
from flask import request
from typing import List, TypeVar


class Auth:
    """ API authentication class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ evaluates if auth is used """
        if path is None:
            return True
        else:
            return False

    def authorization_header(self, request=None) -> str:
        """ Returns the header of each request """
        if request == None:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns the current user """
        return None