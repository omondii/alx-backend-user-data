#!/usr/bin/env python3
""" auth.py """
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """ API authentication class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ evaluates if auth is used """
        if path is None:
            return True
        elif excluded_paths is None and len(excluded_paths) == 0:
            return True
        for p in excluded_paths:
            if p.endswith("*"):
                if path.rstrip('/') == p.rstrip('/'):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Returns the header of each request """
        if request is None:
            return None

        headers = request.headers
        return headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """ Returns the current user """
        return None
    
    def session_cookie(self, request=None):
        """ Returns a cookie value from a request """
        if request is None:
            return None
        else:
            sessId = os.getenv('SESSION_NAME')
            return request.cookies.get(sessId)
