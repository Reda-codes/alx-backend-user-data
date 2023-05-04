#!/usr/bin/env python3
"""
SessionExpAuth class to manage the API authentication
"""
from api.v1.auth.session_auth import SessionAuth
from models.user import User
import uuid
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class that inherits from SessionAuth"""
    def __init__(self):
        """SessionExpAuth class intialization"""
        super().__init__()
        session_duration = os.getenv("SESSION_DURATION")
        try:
            self.session_duration = int(session_duration)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """create_session method"""
        sessionId = super().create_session(user_id)
        if sessionId is None:
            return None
        sessionDictionary = {"user_id": user_id,
                             "created_at": datetime.now()}
        self.user_id_by_session_id[sessionId] = sessionDictionary
        return sessionId

    def user_id_for_session_id(self, session_id=None):
        """user_id_for_session_id method"""
        if session_id is None:
            return None
        dct = self.user_id_by_session_id.get(session_id)
        if dct is None:
            return None
        if self.session_duration <= 0:
            return dct.get("user_id")
        created_at = dct.get("created_at")
        if created_at is None:
            return None
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None
        return dct.get("user_id")
