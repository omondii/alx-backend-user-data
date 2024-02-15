#!/usr/bin/env python3
""" Basic Authentication """
from api.v1.auth.auth import Auth
import base64
import binascii
from typing import Tuple


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
