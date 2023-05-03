#!/usr/bin/env python3
"""
SessionAuth class to manage the API authentication
"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """SessionAuth class that inherits from Auth"""
    def __init__(self):
        """class Initialization"""
        self.user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create_session method"""
        if user_id is None or not isinstance(user_id, str):
            return None
        else:
            sessionId = str(uuid.uuid4())
            self.user_id_by_session_id[sessionId] = user_id
            return sessionId

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """create_session method """
        if session_id is None or not isinstance(session_id, str):
            return None
        else:
            userId = self.user_id_by_session_id.get(session_id)
            return userId
