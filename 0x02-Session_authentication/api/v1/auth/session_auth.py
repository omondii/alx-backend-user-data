#!/usr/bin/env python3
""" sessionAuth inherits from Auth """
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """ Session Auth class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a session ID for a user_id """
        if user_id is None or not isinstance(user_id, str):
            return None
        else:
            sessionId = str(uuid.uuid4())
            self.user_id_by_session_id[sessionId] = user_id
            return sessionId

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a user Id based on sessionId """
        if session_id is None or not isinstance(session_id, str):
            return None
        else:
            UserId = self.user_id_by_session_id.get(session_id)
            return UserId