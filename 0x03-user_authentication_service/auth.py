#!/usr/bin/env python
"""
auth module
"""
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """ Method that takes string arguments and returns bytes """
    salt = b'$2b$12$eUDdeuBtrD41c8dXvzh95eh'
    return bcrypt.hashpw(password.encode(), salt)

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Method to regester a new user """
