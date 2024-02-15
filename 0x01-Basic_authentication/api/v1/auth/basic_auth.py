#!/usr/bin/env python3
""" Basic Authentication """
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ BAsic Auth integration """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
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
