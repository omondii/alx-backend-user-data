#!/usr/bin/env python3
""" Basic Authentication """
from api.v1.auth.auth import Auth
import base64
import binascii
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """ BAsic Auth integration """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ Returns the base64 part of the Auth header """
        if authorization_header is None or not\
                isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        if authorization_header.find('Basic ') == -1:
            return None

        authed = authorization_header[authorization_header.find('Basic ')+6:]
        return authed

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Returns the decoded value of Base64 string """
        if base64_authorization_header is None or\
                not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded = base64.b64decode(base64_authorization_header)\
                .decode('utf-8')
            return decoded
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
                                decode_base64_authorization_header: str)\
                                -> tuple:  # type: ignore
        """ Returns the user email and pwd from decoded value """
        if decode_base64_authorization_header is None or not\
                isinstance(decode_base64_authorization_header, str):
            return (None, None)
        if ":" not in decode_base64_authorization_header:
            return (None, None)

        data = decode_base64_authorization_header.split(":")
        return tuple(data)
        """
        email = data[0]
        pwd = ":".join(data[1:])

        cred = (email, pwd)
        return cred
        """

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'): # type: ignore
        """ Returns the User instance based on email & password """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        user = User.search({"email": user_email})
        try:
            if user:
                if user[0].is_valid_password(user_pwd):
                    return user[0]
                return None
        except KeyError:
            return None
        
    def current_user(self, request=None) -> TypeVar('User'): # type: ignore
        """ Overloads Auth and returns the User instance for a request """
        if request is None:
            return None

        auth_header = self.authorization_header(request)
        extractedHeader = self.extract_base64_authorization_header(auth_header)
        decodedHeader = self.decode_base64_authorization_header(extractedHeader)
        email, pwd = self.extract_user_credentials(decodedHeader)
        return self.user_object_from_credentials(email, pwd)