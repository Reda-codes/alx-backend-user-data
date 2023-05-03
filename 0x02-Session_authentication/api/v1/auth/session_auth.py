#!/usr/bin/env python3
"""
SessionAuth class to manage the API authentication
"""
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """SessionAuth class that inherits from Auth"""
