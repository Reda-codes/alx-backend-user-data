#!/usr/bin/env python3
"""
SessionDBAuth class to manage the API authentication
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import uuid
import os
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class that inherits from SessionExpAuth"""
    def create_session(self, user_id=None):
        """ create_session method """
        sessionId = super().create_session(user_id)
        if sessionId is None:
            return None
        userSession = UserSession(user_id=user_id,
                                  session_id=str(uuid.uuid4()))
        return userSession.session_id

    def user_id_for_session_id(self, session_id=None):
        """user_id_for_session_id method"""
        if session_id is None:
            return None
        dct = UserSession.search({"session_id": session_id})
        if dct is None:
            return None
        if self.session_duration <= 0:
            return dct[0].get("user_id")
        created_at = dct[0].get("created_at")
        if created_at is None:
            return None
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None
        return dct[0].get("user_id")

    def destroy_session(self, request=None):
        """destroy_session method"""
        if request is None:
            return False
        sessionId = self.session_cookie(request)
        if not sessionId:
            return False
        dct = UserSession.search({"session_id": session_id})
        userId = dct[0].get("user_id")
        if not userId:
            return False
        dct[0].remove()
        return True
